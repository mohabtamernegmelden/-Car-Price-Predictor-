import numpy as np
import pandas as pd
import pickle
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Churn Prediction",
    page_icon="🔮",
    layout="wide"
)

def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');

    :root {
      --bg:          #050c14;
      --bg-card:     #0a1628;
      --bg-surface:  #0f1f38;
      --border:      #1a3050;
      --accent:      #00c8ff;
      --accent-dim:  #0099cc;
      --accent-soft: #00c8ff18;
      --success:     #00e5a0;
      --success-bg:  #00e5a012;
      --danger:      #ff3c6e;
      --danger-bg:   #ff3c6e12;
      --warn:        #ffb740;
      --warn-bg:     #ffb74012;
      --text-primary:   #e8f4ff;
      --text-secondary: #7a9ab8;
      --text-muted:     #3d5a78;
      --radius: 6px;
      --radius-lg: 12px;
    }

    html, body, [class*="css"] {
      font-family: 'JetBrains Mono', monospace !important;
      background-color: var(--bg) !important;
      color: var(--text-primary) !important;
    }

    .stApp {
      background-color: var(--bg) !important;
      background-image:
        linear-gradient(var(--border) 1px, transparent 1px),
        linear-gradient(90deg, var(--border) 1px, transparent 1px);
      background-size: 40px 40px;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
      padding: 2rem 3rem 4rem !important;
      max-width: 1000px !important;
    }

    /* ── HERO ── */
    .hero {
      position: relative;
      text-align: center;
      padding: 3rem 2rem 2.5rem;
      margin-bottom: 2.5rem;
      border-bottom: 1px solid var(--border);
      overflow: hidden;
    }
    .hero::before {
      content: '';
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse 70% 60% at 50% 0%, #00c8ff18 0%, transparent 70%);
      pointer-events: none;
    }
    .hero::after {
      content: 'CHURN.AI';
      position: absolute;
      bottom: -0.5rem;
      right: 2rem;
      font-family: 'Syne', sans-serif;
      font-size: 5rem;
      font-weight: 800;
      color: var(--text-muted);
      opacity: 0.1;
      letter-spacing: -0.02em;
      pointer-events: none;
    }
    .hero h1 {
      font-family: 'Syne', sans-serif !important;
      font-size: 2.4rem !important;
      font-weight: 800 !important;
      background: linear-gradient(135deg, #ffffff 30%, var(--accent)) !important;
      -webkit-background-clip: text !important;
      -webkit-text-fill-color: transparent !important;
      background-clip: text !important;
      margin: 0 0 0.6rem !important;
      line-height: 1.1 !important;
    }
    .hero p {
      color: var(--text-secondary) !important;
      font-size: 0.82rem !important;
      letter-spacing: 0.14em !important;
      text-transform: uppercase !important;
      margin: 0 !important;
    }

    /* ── SECTION HEADING ── */
    .section-heading {
      font-family: 'Syne', sans-serif;
      font-size: 0.7rem;
      font-weight: 700;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--accent);
      border-left: 3px solid var(--accent);
      padding-left: 0.75rem;
      margin: 1.5rem 0 1rem;
    }

    /* ── LABELS ── */
    label, p {
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 0.72rem !important;
      font-weight: 500 !important;
      letter-spacing: 0.08em !important;
      text-transform: uppercase !important;
      color: var(--text-secondary) !important;
    }

    /* ── SELECTBOX ── */
    div[data-baseweb="select"] > div {
      background-color: var(--bg-surface) !important;
      border: 1px solid var(--border) !important;
      border-radius: var(--radius) !important;
      color: var(--text-primary) !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 0.82rem !important;
      transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    div[data-baseweb="select"] > div:hover {
      border-color: var(--accent-dim) !important;
      box-shadow: 0 0 0 3px var(--accent-soft) !important;
    }
    div[data-baseweb="select"] > div:focus-within {
      border-color: var(--accent) !important;
      box-shadow: 0 0 0 3px var(--accent-soft) !important;
    }
    div[data-baseweb="popover"] {
      background: var(--bg-surface) !important;
      border: 1px solid var(--border) !important;
      border-radius: var(--radius) !important;
      box-shadow: 0 24px 48px #00000080 !important;
    }
    div[role="option"] {
      background: transparent !important;
      color: var(--text-secondary) !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 0.8rem !important;
    }
    div[role="option"]:hover,
    div[role="option"][aria-selected="true"] {
      background: var(--accent-soft) !important;
      color: var(--accent) !important;
    }

    /* ── NUMBER INPUT ── */
    input[type="number"] {
      background: var(--bg-surface) !important;
      border: 1px solid var(--border) !important;
      border-radius: var(--radius) !important;
      color: var(--text-primary) !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 0.85rem !important;
      transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    input[type="number"]:focus {
      border-color: var(--accent) !important;
      box-shadow: 0 0 0 3px var(--accent-soft) !important;
      outline: none !important;
    }
    .stNumberInput button {
      background: var(--bg-surface) !important;
      border-color: var(--border) !important;
      color: var(--text-secondary) !important;
    }

    /* ── PREDICT BUTTON ── */
    .stButton > button {
      font-family: 'Syne', sans-serif !important;
      font-size: 0.95rem !important;
      font-weight: 700 !important;
      letter-spacing: 0.15em !important;
      text-transform: uppercase !important;
      background: transparent !important;
      color: var(--accent) !important;
      border: 1.5px solid var(--accent) !important;
      border-radius: var(--radius) !important;
      padding: 0.75rem 2.5rem !important;
      width: 100% !important;
      margin-top: 1.5rem !important;
      transition: color 0.25s, background 0.25s, box-shadow 0.25s !important;
    }
    .stButton > button:hover {
      background: var(--accent) !important;
      color: var(--bg) !important;
      box-shadow: 0 0 28px var(--accent-dim) !important;
    }

    /* ── RESULT CARDS ── */
    .error-box {
      background: var(--danger-bg);
      border: 1px solid var(--danger);
      border-left: 4px solid var(--danger);
      border-radius: var(--radius-lg);
      padding: 1.4rem 1.8rem;
      margin: 1.5rem 0 0.5rem;
      animation: slideIn 0.4s cubic-bezier(0.2,0.8,0.3,1);
    }
    .error-box h3 {
      font-family: 'Syne', sans-serif !important;
      font-size: 1.1rem !important;
      font-weight: 700 !important;
      color: var(--danger) !important;
      margin: 0 !important;
    }
    .success-box {
      background: var(--success-bg);
      border: 1px solid var(--success);
      border-left: 4px solid var(--success);
      border-radius: var(--radius-lg);
      padding: 1.4rem 1.8rem;
      margin: 1.5rem 0 0.5rem;
      animation: slideIn 0.4s cubic-bezier(0.2,0.8,0.3,1);
    }
    .success-box h3 {
      font-family: 'Syne', sans-serif !important;
      font-size: 1.1rem !important;
      font-weight: 700 !important;
      color: var(--success) !important;
      margin: 0 !important;
    }

    /* probability text */
    .prob-display {
      font-family: 'Syne', sans-serif;
      font-size: 1.4rem;
      font-weight: 700;
      color: var(--text-primary);
      margin: 1rem 0 0.5rem;
    }
    .prob-display span {
      color: var(--accent);
    }

    /* ── ALERTS ── */
    div[data-testid="stWarning"] {
      background: var(--warn-bg) !important;
      border: 1px solid var(--warn) !important;
      color: var(--warn) !important;
      border-radius: var(--radius) !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 0.82rem !important;
    }
    div[data-testid="stInfo"] {
      background: #00c8ff0d !important;
      border: 1px solid var(--accent) !important;
      color: var(--accent) !important;
      border-radius: var(--radius) !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 0.82rem !important;
    }
    div[data-testid="stSuccess"] {
      background: var(--success-bg) !important;
      border: 1px solid var(--success) !important;
      color: var(--success) !important;
      border-radius: var(--radius) !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 0.82rem !important;
    }
    div[data-testid="stError"] {
      background: var(--danger-bg) !important;
      border: 1px solid var(--danger) !important;
      color: var(--danger) !important;
      border-radius: var(--radius) !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 0.82rem !important;
    }

    /* ── DIVIDER ── */
    hr {
      border-color: var(--border) !important;
      margin: 1.5rem 0 !important;
    }

    /* ── SCROLLBAR ── */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 99px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-dim); }

    @keyframes slideIn {
      from { opacity: 0; transform: translateY(12px); }
      to   { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)

load_css()


BASE_DIR = Path(__file__).resolve().parent
path = BASE_DIR / 'models' / 'Customer_Churn_Model.pkl'

with open(path, 'rb') as f:
    model_data = pickle.load(f)

model        = model_data['model']
feature_names = model_data['features_names']
encoder_col  = model_data['encoder_col']

def prediction(input_data):
    input_df = pd.DataFrame([input_data])

    for column in encoder_col.keys():
        if column in input_df.columns:
            try:
                input_df[column] = encoder_col[column].transform(input_df[column])
            except ValueError:
                st.error(f"Unknown category detected in column: {column}")
                return

    input_df = input_df.reindex(columns=feature_names)
    numeric_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
    input_df[numeric_cols] = input_df[numeric_cols].astype(float)

    pred       = model.predict(input_df)[0]
    pred_proba = model.predict_proba(input_df)[0][1]

    if pred == 1:
        st.markdown("""
        <div class="error-box">
            <h3>🚨 High Risk — Customer WILL Churn</h3>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box">
            <h3>✅ Low Risk — Customer will NOT Churn</h3>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="prob-display">Churn Probability: <span>{pred_proba:.2%}</span></div>
    """, unsafe_allow_html=True)

    if pred_proba >= 0.7:
        st.warning("⚠️  High Risk Customer — Immediate action recommended")
    elif pred_proba >= 0.4:
        st.info("ℹ️  Moderate Risk Customer — Monitor closely")
    else:
        st.success("✅  Low Risk Customer — Retention looks strong")

def main():
    st.markdown("""
    <div class="hero">
        <h1>Customer Churn Prediction</h1>
        <p>AI-powered system · Predict customer retention risk</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">Customer Profile</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        gender        = st.selectbox('Gender', ('Female', 'Male'))
    with col2:
        SeniorCitizen = st.selectbox('Senior Citizen', ('No', 'Yes'))
        SeniorCitizen = 1 if SeniorCitizen == 'Yes' else 0
    with col3:
        tenure        = st.number_input('Tenure (Months)', min_value=0)

    col4, col5 = st.columns(2)
    with col4:
        Partner    = st.selectbox('Partner', ('No', 'Yes'))
    with col5:
        Dependents = st.selectbox('Dependents', ('No', 'Yes'))

    st.markdown('<div class="section-heading">Services</div>', unsafe_allow_html=True)
    col6, col7, col8 = st.columns(3)
    with col6:
        PhoneService  = st.selectbox('Phone Service', ('No', 'Yes'))
        MultipleLines = st.selectbox('Multiple Lines', ('No', 'Yes', 'No phone service'))
    with col7:
        InternetService  = st.selectbox('Internet Service', ('DSL', 'Fiber optic', 'No'))
        OnlineSecurity   = st.selectbox('Online Security', ('No', 'Yes', 'No internet service'))
        OnlineBackup     = st.selectbox('Online Backup', ('No', 'Yes', 'No internet service'))
    with col8:
        DeviceProtection = st.selectbox('Device Protection', ('No', 'Yes', 'No internet service'))
        TechSupport      = st.selectbox('Tech Support', ('No', 'Yes', 'No internet service'))
        StreamingTV      = st.selectbox('Streaming TV', ('No', 'Yes', 'No internet service'))
        StreamingMovies  = st.selectbox('Streaming Movies', ('No', 'Yes', 'No internet service'))

    st.markdown('<div class="section-heading">Billing & Contract</div>', unsafe_allow_html=True)
    col9, col10 = st.columns(2)
    with col9:
        Contract         = st.selectbox('Contract Type', ('Month-to-month', 'One year', 'Two year'))
        PaperlessBilling = st.selectbox('Paperless Billing', ('No', 'Yes'))
    with col10:
        PaymentMethod = st.selectbox(
            'Payment Method',
            ('Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)')
        )

    col11, col12 = st.columns(2)
    with col11:
        MonthlyCharges = st.number_input('Monthly Charges ($)', min_value=0.0, format="%.2f")
    with col12:
        TotalCharges   = st.number_input('Total Charges ($)', min_value=0.0, format="%.2f")

    input_data = {
        'gender': gender, 'SeniorCitizen': SeniorCitizen,
        'Partner': Partner, 'Dependents': Dependents, 'tenure': tenure,
        'PhoneService': PhoneService, 'MultipleLines': MultipleLines,
        'InternetService': InternetService, 'OnlineSecurity': OnlineSecurity,
        'OnlineBackup': OnlineBackup, 'DeviceProtection': DeviceProtection,
        'TechSupport': TechSupport, 'StreamingTV': StreamingTV,
        'StreamingMovies': StreamingMovies, 'Contract': Contract,
        'PaperlessBilling': PaperlessBilling, 'PaymentMethod': PaymentMethod,
        'MonthlyCharges': MonthlyCharges, 'TotalCharges': TotalCharges
    }

    if st.button('🔮  Run Prediction'):
        prediction(input_data)

if __name__ == '__main__':
    main()