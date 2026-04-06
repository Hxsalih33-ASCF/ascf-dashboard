import streamlit as st
import numpy as np

# Title and Academic Context
st.set_page_config(page_title="ASCF Dashboard", layout="wide")
st.title("Algorithmic Stewardship Capacity (ASCF) Dashboard")
st.markdown("Interactive Systemic Risk & Governance Deficit ($\Delta G$) Calculator")

# Sidebar for 5-Pillar Inputs
st.sidebar.header("Institutional Parameters (Inputs)")
HOL = st.sidebar.slider("Human-in-the-Loop (HOL)", 0.0, 1.0, 0.75)
L   = st.sidebar.slider("Algorithmic Literacy (L)", 0.0, 1.0, 0.71)
Eth = st.sidebar.slider("Ethical Cohesion (Eth)", 0.0, 1.0, 0.80)
Gov = st.sidebar.slider("Institutional Governance (Gov)", 0.0, 1.0, 0.77)
Reg = st.sidebar.slider("Regulatory Enforcement (Reg)", 0.0, 1.0, 0.80)

# ASCF Mathematical Engine
k = 8.0
h0 = 0.55
f_HOL = 1.0 / (1.0 + np.exp(-k * (HOL - h0)))
Total_Sc = f_HOL * (L**0.70) * (Eth**1.20) * (Gov**0.80) * (Reg**0.90)

# Display Current Capacity
st.subheader("1. Systemic Capacity Output")
col1, col2 = st.columns(2)
col1.metric(label="Barrier of Agency (f_HOL)", value=f"{f_HOL:.4f}")
col2.metric(label="Total Stewardship Capacity (Sc)", value=f"{Total_Sc:.4f}")

if Total_Sc < 0.10:
    st.error("⚠️ SYSTEM DEFICIT: Structural capacity is near-zero due to weak-link failure.")
else:
    st.success("✅ SYSTEM STABLE: Institutional structures are supporting human oversight.")

# Governance Deficit Calculator
st.subheader("2. Governance Deficit Matrix ($\Delta G$)")
st.markdown("Test this institutional environment against specific AI complexity levels.")

# Added Canonical Cases per Antigravity Review
ai_systems = {
    "National Biometric ID": 16.50,
    "COMPAS (Recidivism)": 14.31,
    "IBM Watson for Oncology ":9.0,
    "SyRI (Welfare Fraud)": 11.59,
  "SEC PDA Governance Anchor ":5.7,
    "Automated Tax Auditing": 11.59,
    "Predictive Credit Scoring": 9.20,
    "IBM Watson Health": 8.76,
    "Amazon HR Algorithmic Resume": 7.2,
    "Generative Financial LLM (SEC)": 5.70
}

selected_ai = st.selectbox("Select AI System to Deploy:", list(ai_systems.keys()))
tlari = ai_systems[selected_ai]
lam = 0.50
req_sc = lam * np.log(tlari)

# Fixed Sign Convention: Delta G is now positive for deficits
delta_g = req_sc - Total_Sc

st.write(f"**TLARI Score for {selected_ai}:** {tlari}")
st.write(f"**Required Capacity:** {req_sc:.4f}")

if delta_g > 0:
    st.error(f"🚨 **Governance Deficit ($\Delta G$): {delta_g:.4f}** (Calculated as Required Capacity - Sc. A positive value confirms the system complexity exceeds capacity.)")
else:
    st.success(f"🛡️ **Surplus Capacity:** {abs(delta_g):.4f} (The institution can safely govern this AI)")

# Added Official Citation Panel
st.markdown("---")
st.caption("ASCF Dashboard v1.0 | Salihu, H. (2026). Algorithmic Stewardship Competency Framework, Tarrant County College District | MC seed=20260307 | Parameters: α=0.70, βe=1.20, γg=0.80, δr=0.90, λ=0.50")