import plotly.graph_objects as go

HOURS = list(range(73))

PLOT_DEFAULTS = dict(
    plot_bgcolor="#ffffff",
    paper_bgcolor="#f1f5f9",
    font=dict(family="Inter", size=12, color="#1e293b"),
    margin=dict(l=10, r=10, t=10, b=10),
    xaxis=dict(gridcolor="#f1f5f9", linecolor="#e2e8f0"),
    yaxis=dict(gridcolor="#f1f5f9", linecolor="#e2e8f0"),
)

def strength_chart(phys, ml, req_str, stm_dur):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=HOURS, y=[req_str] * 73, name="Target",
        mode="lines", line=dict(color="#94a3b8", width=1.5, dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x=HOURS, y=phys, name="Physics (Nurse-Saul)",
        mode="lines", line=dict(color="#003366", width=2.5)
    ))
    fig.add_trace(go.Scatter(
        x=HOURS, y=ml, name="ML Prediction",
        mode="lines", line=dict(color="#FFD700", width=3)
    ))
    fig.add_vline(
        x=stm_dur, line_dash="dot", line_color="#10b981",
        annotation_text="Steam End",
        annotation_font_color="#10b981",
        annotation_font_size=11
    )
    fig.update_layout(
        **PLOT_DEFAULTS,
        xaxis_title="Hours",
        yaxis_title="Compressive Strength (MPa)",
        legend=dict(orientation="h", y=-0.25, font=dict(color="#1e293b")),
        height=320,
    )
    return fig

def tradeoff_chart(dur_range, strengths, energies, req_str, opt_dur):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(dur_range), y=list(strengths),
        name="Predicted Strength (MPa)",
        mode="lines", line=dict(color="#003366", width=2.5)
    ))
    fig.add_trace(go.Scatter(
        x=list(dur_range), y=energies,
        name="Energy Cost (relative)",
        mode="lines", line=dict(color="#f97316", width=2, dash="dot"),
        yaxis="y2"
    ))
    fig.add_hline(
        y=req_str, line_dash="dash", line_color="#10b981",
        annotation_text=f"Required: {req_str} MPa",
        annotation_font_color="#10b981",
        annotation_font_size=11
    )
    if opt_dur:
        fig.add_vline(
            x=opt_dur, line_dash="dot", line_color="#6366f1",
            annotation_text=f"Optimal: {opt_dur:.1f}h",
            annotation_font_color="#6366f1",
            annotation_font_size=11
        )
    fig.update_layout(
        plot_bgcolor="#ffffff",
        paper_bgcolor="#f1f5f9",
        font=dict(family="Inter", size=12, color="#1e293b"),
        margin=dict(l=10, r=10, t=10, b=10),
        xaxis=dict(title="Steam Duration (hours)", gridcolor="#f1f5f9", linecolor="#e2e8f0"),
        yaxis=dict(title="Strength (MPa)", gridcolor="#f1f5f9",
                   title_font=dict(color="#003366")),
        yaxis2=dict(title="Energy Cost", overlaying="y", side="right",
                    showgrid=False, title_font=dict(color="#f97316")),
        legend=dict(orientation="h", y=-0.3, font=dict(color="#1e293b")),
        height=300,
    )
    return fig