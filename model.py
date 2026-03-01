import numpy as np
import streamlit as st
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from physics import T_DATUM, HOURS, maturity, temp_profile

@st.cache_resource
def train_model():
    np.random.seed(42)
    n = 1500
    wc   = np.random.uniform(0.30, 0.60, n)
    scm  = np.random.uniform(0,    40,   n)
    sd   = np.random.uniform(4,    24,   n)
    st_  = np.random.uniform(50,   80,   n)
    adm  = np.random.uniform(0,     5,   n)
    amb  = np.random.uniform(15,   45,   n)
    mat  = (st_ - T_DATUM) * sd * (1 + 0.01 * amb)
    fc28 = np.clip(55 - 60 * (wc - 0.30) + 0.3 * scm, 20, 70)
    y    = np.clip(
        fc28 * (1 - np.exp(-0.0048 * mat)) + adm * 1.1 + np.random.normal(0, 1.5, n),
        5, 75
    )
    X = np.column_stack([wc, scm, sd, st_, adm, amb, mat])
    pipe = Pipeline([
        ("sc", StandardScaler()),
        ("gb", GradientBoostingRegressor(
            n_estimators=200, max_depth=4,
            learning_rate=0.06, random_state=42
        ))
    ])
    pipe.fit(X, y)
    return pipe

def ml_curve(model, wc, scm, stm_dur, stm_temp, admix, amb_temp, mats, fc28):
    X = np.array([
        [wc, scm, min(h, stm_dur), stm_temp, admix, amb_temp, mats[h]]
        for h in HOURS
    ])
    return np.clip(model.predict(X), 0, fc28 * 1.1).tolist()

def predict_single(model, wc, scm, stm_dur, stm_temp, admix, amb_temp, mat_val, fc28):
    X = np.array([[wc, scm, stm_dur, stm_temp, admix, amb_temp, mat_val]])
    return float(np.clip(model.predict(X)[0], 0, fc28 * 1.1))

def optimization_sweep(model, wc, scm, stm_temp, admix, amb_temp, fc28):
    dur_range = np.linspace(4, 24, 80)
    strengths, energies = [], []
    for d in dur_range:
        tp  = temp_profile(amb_temp, stm_temp, d)
        mt  = maturity(tp)
        xi  = np.array([[wc, scm, d, stm_temp, admix, amb_temp, mt[int(d)]]])
        s   = float(np.clip(model.predict(xi)[0], 0, fc28 * 1.1))
        strengths.append(s)
        energies.append(d * stm_temp * 0.85)
    return dur_range, np.array(strengths), energies