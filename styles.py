CSS = """
<style>
  [data-testid="stAppViewContainer"] { background: #f1f5f9; }

  [data-testid="stSidebar"] { background: #003366 !important; }
  [data-testid="stSidebar"] label { color: #FFD700 !important; font-weight: 600; font-size: 13px; }
  [data-testid="stSidebar"] p     { color: #cbd5e1 !important; font-size: 12px; }
  [data-testid="stSidebar"] span  { color: #ffffff !important; }
  [data-testid="stSidebar"] h2    { color: #ffffff !important; }
  [data-testid="stSidebar"] h3    { color: #FFD700 !important; }
  [data-testid="stSidebar"] [data-testid="stSliderValue"] { color: #ffffff !important; }

  .card {
    background: #ffffff;
    border-radius: 10px;
    padding: 20px 22px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    margin-bottom: 4px;
  }
  .card-label {
    font-size: 11px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
  }
  .card-value {
    font-size: 26px;
    font-weight: 800;
    margin-bottom: 4px;
  }
  .card-sub { font-size: 12px; color: #64748b; }

  .section-title {
    font-size: 14px;
    font-weight: 700;
    color: #003366;
    border-left: 4px solid #FFD700;
    padding-left: 10px;
    margin: 20px 0 12px 0;
  }
  .insight {
    background: #ffffff;
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 13px;
    color: #1e293b;
    border-left: 4px solid #003366;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
  }
  .insight b { color: #003366; }

  .footer {
    background: #003366;
    border-radius: 10px;
    padding: 14px 22px;
    margin-top: 24px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .footer-left  { color: #94a3b8; font-size: 12px; }
  .footer-right { color: #FFD700; font-size: 13px; font-weight: 700; text-align: right; }
  .footer-right span { display: block; color: #ffffff; font-size: 11px; font-weight: 400; }
</style>
"""

HEADER_HTML = """
<div style="background:#003366;border-radius:10px;padding:16px 24px;margin-bottom:20px;
            display:flex;align-items:center;justify-content:space-between;">
  <div>
    <div style="color:#ffffff;font-size:22px;font-weight:800;letter-spacing:0.5px;">CureLogic</div>
    <div style="color:#FFD700;font-size:11px;letter-spacing:1.5px;margin-top:2px;">
      L&T CREATECH 2026 — PHYSICS-INFORMED AI CURING PLATFORM
    </div>
  </div>
  <div style="color:#94a3b8;font-size:12px;text-align:right;">
    Gradient Boosting + Nurse-Saul Maturity<br>
    <span style="color:#10b981;">DIGITAL TWIN ACTIVE</span>
  </div>
</div>
"""

FOOTER_HTML = """
<div class="footer">
  <div class="footer-left">
    CureLogic uses a physics-informed ML model calibrated to the Nurse-Saul Maturity Method
    to predict and optimize concrete curing cycles.
  </div>
  <div class="footer-right">
    CureLogic v2.0
    <span>L&T CreaTech 2026</span>
  </div>
</div>
"""

def kpi_card_html(label, value, sub, color):
    return f"""
    <div class="card" style="border-top:4px solid {color};">
      <div class="card-label">{label}</div>
      <div class="card-value" style="color:{color};">{value}</div>
      <div class="card-sub">{sub}</div>
    </div>"""

def insight_html(title, body):
    return f'<div class="insight"><b>{title}</b><br><br>{body}</div>'

def section_title_html(text):
    return f'<div class="section-title">{text}</div>'