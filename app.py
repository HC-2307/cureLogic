import streamlit as st
import pandas as pd
import numpy as np

from physics import temp_profile, maturity, physics_curve, estimate_fc28, HOURS
from model import train_model, ml_curve, predict_single, optimization_sweep
from charts import strength_chart, tradeoff_chart
from styles import (CSS, HEADER_HTML, FOOTER_HTML,
                    kpi_card_html, insight_html, section_title_html)

st.set_page_config(
    page_title="CureLogic | L&T CreaTech 2026",
    page_icon="🏗️",
    layout="wide",
)

st.markdown(CSS, unsafe_allow_html=True)
st.markdown(HEADER_HTML, unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## CureLogic")
    st.markdown("### Mix Design")
    wc       = st.slider("Water-Cement Ratio",   0.30, 0.60, 0.42, 0.01)
    scm      = st.slider("SCM Content (%)",      0,    40,   20)
    admix    = st.slider("Admixture (%)",        0.0,  5.0,  2.0, 0.1)
    st.markdown("### Curing Regime")
    amb_temp = st.slider("Ambient Temp (°C)",    15,   45,   28)
    stm_temp = st.slider("Steam Temp (°C)",      50,   80,   65)
    stm_dur  = st.slider("Steam Duration (hrs)", 4,    24,   12)
    st.markdown("### Target")
    req_str  = st.slider("Required Strength (MPa)", 15, 60, 30)

# ── Compute ────────────────────────────────────────────────────────────────────
model    = train_model()
fc28     = estimate_fc28(wc, scm, admix)
temps    = temp_profile(amb_temp, stm_temp, stm_dur)
mats     = maturity(temps)
phys     = physics_curve(temps, mats, fc28)
ml       = ml_curve(model, wc, scm, stm_dur, stm_temp, admix, amb_temp, mats, fc28)

dur_range, opt_strengths, opt_energies = optimization_sweep(
    model, wc, scm, stm_temp, admix, amb_temp, fc28
)
valid    = opt_strengths >= req_str
opt_dur  = float(dur_range[valid][0]) if valid.any() else None

pred_str = predict_single(model, wc, scm, stm_dur, stm_temp, admix, amb_temp, mats[stm_dur], fc28)
is_ready = pred_str >= req_str

base_nrg    = 24 * stm_temp * 0.85
opt_nrg     = (opt_dur or stm_dur) * stm_temp * 0.85
nrg_saving  = (base_nrg - opt_nrg) / base_nrg * 100

# ── KPI Cards ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
cards = [
    (c1, "Predicted Strength",      f"{pred_str:.1f} MPa",
     f"Physics: {phys[stm_dur]:.1f} MPa  |  Target: {req_str} MPa", "#003366"),
    (c2, "Curing Status",
     "READY" if is_ready else "CURING",
     "Threshold met" if is_ready else f"Deficit: {req_str - pred_str:.1f} MPa",
     "#10b981" if is_ready else "#f59e0b"),
    (c3, "Optimal Steam Duration",
     f"{opt_dur:.1f} hrs" if opt_dur else "N/A",
     f"Current: {stm_dur} hrs  |  Save: {max(0, stm_dur - (opt_dur or stm_dur)):.1f} hrs", "#6366f1"),
    (c4, "Energy Saving",           f"{nrg_saving:.1f}%",
     "vs. 24-hr baseline regime", "#059669"),
]
for col, label, value, sub, color in cards:
    col.markdown(kpi_card_html(label, value, sub, color), unsafe_allow_html=True)

# ── Strength Chart ─────────────────────────────────────────────────────────────
st.markdown(section_title_html("Strength Gain Curve"), unsafe_allow_html=True)
st.plotly_chart(strength_chart(phys, ml, req_str, stm_dur), use_container_width=True)

# ── Tradeoff + Table ───────────────────────────────────────────────────────────
st.markdown(section_title_html("Optimization and Summary"), unsafe_allow_html=True)
col_chart, col_table = st.columns([3, 2])

with col_chart:
    st.plotly_chart(
        tradeoff_chart(dur_range, opt_strengths, opt_energies, req_str, opt_dur),
        use_container_width=True
    )

with col_table:
    key_hrs = [0, 4, 8, 12, 16, 20, 24, 36, 48, 72]
    rows = [{
        "Hour":        h,
        "Temp (C)":    f"{temps[h]:.1f}",
        "Maturity":    f"{mats[h]:.0f}",
        "Physics MPa": f"{phys[h]:.1f}",
        "ML MPa":      f"{ml[h]:.1f}",
        "Ready":       "Yes" if ml[h] >= req_str else "No"
    } for h in key_hrs]
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True, height=300)

# ── Insights ───────────────────────────────────────────────────────────────────
st.markdown(section_title_html("Recommendations"), unsafe_allow_html=True)
i1, i2, i3 = st.columns(3)

with i1:
    if opt_dur and opt_dur < stm_dur:
        msg = (f"Target met at {stm_dur}h. Minimum required duration is "
               f"<b>{opt_dur:.1f}h</b>, saving <b>{stm_dur - opt_dur:.1f}h</b> of steam time.")
    elif opt_dur:
        msg = (f"Increase steam duration to at least <b>{opt_dur:.1f}h</b> "
               f"to achieve the required {req_str} MPa.")
    else:
        msg = (f"Required strength of <b>{req_str} MPa</b> is not achievable. "
               f"Reduce W/C ratio or increase steam temperature.")
    st.markdown(insight_html("Cycle Optimization", msg), unsafe_allow_html=True)

with i2:
    wc_opt = max(0.30, wc - 0.03)
    gain   = 60 * 0.03
    st.markdown(insight_html(
        "Mix Design Suggestion",
        f"Reducing W/C ratio from <b>{wc:.2f}</b> to <b>{wc_opt:.2f}</b> can improve "
        f"28-day strength by approximately <b>{gain:.1f} MPa</b>."
    ), unsafe_allow_html=True)

with i3:
    st.markdown(insight_html(
        "Model Info",
        "Gradient Boosting Regressor trained on 1,500 synthetic curing cycles. "
        "Features: W/C ratio, SCM, steam duration, steam temp, admixture, ambient temp, maturity index."
    ), unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(FOOTER_HTML, unsafe_allow_html=True)