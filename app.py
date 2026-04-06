import streamlit as st
import numpy as np
import pandas as pd

# Title and Academic Context
st.set_page_config(page_title="ASCF Dashboard v2.0", layout="wide")
st.title("Algorithmic Stewardship Capacity (ASCF) Dashboard")
st.markdown("Interactive Systemic Risk, Governance Deficit ($\Delta G$), and Stochastic Stress Testing")

# Sidebar for 5-Pillar Inputs
st.sidebar.header("Institutional Parameters (Inputs)")
st.sidebar.markdown("Adjust these sliders to set the baseline environment.")
HOL = st.sidebar.slider("Human-in-the-Loop (HOL)", 0.0, 1.0, 0.75)
L   = st.sidebar.slider("Algorithmic Literacy (L)", 0.0, 1.0, 0.71)
Eth = st.sidebar.slider("Ethical Cohesion (Eth)", 0.0, 1.0, 0.80)
Gov = st.sidebar.slider("Institutional Governance (Gov)", 0.0, 1.0, 0.77)
Reg = st.sidebar.slider("Regulatory Enforcement (Reg)", 0.0, 1.0, 0.80)

# ASCF Mathematical Engine (Deterministic)
k = 8.0
h0 = 0.55
f_HOL = 1.0 / (1.0 + np.exp(-k * (HOL - h0)))
Total_Sc = f_HOL * (L**0.70) * (Eth**1.20) * (Gov**0.80) * (Reg**0.90)

# Display Current Capacity
st.subheader("1. Static Systemic Capacity Output")
col1, col2 = st.columns(2)
col1.metric(label="Barrier of Agency (f_HOL)", value=f"{f_HOL:.4f}")
col2.metric(label="Total Stewardship Capacity (Sc)", value=f"{Total_Sc:.4f}")

if Total_Sc < 0.10:
    st.error("⚠️ SYSTEM DEFICIT: Structural capacity is near-zero due to weak-link failure.")
else:
    st.success("✅ SYSTEM STABLE: Institutional structures are supporting human oversight.")

# Governance Deficit Calculator
st.subheader("2. Governance Deficit Matrix ($\Delta G$)")
ai_systems = {
    "National Biometric ID": 16.50,
    "COMPAS (Recidivism)": 14.31,
    "SyRI (Welfare Fraud)": 11.59,
    "Automated Tax Auditing": 11.59,
    "Predictive Credit Scoring": 9.20,
    "IBM Watson Health": 8.76,
    "Amazon HR Algorithmic Resume": 7.16,
    "Generative Financial LLM (SEC)": 5.70
}

selected_ai = st.selectbox("Select AI System to Deploy:", list(ai_systems.keys()))
tlari = ai_systems[selected_ai]
lam = 0.50
req_sc = lam * np.log(tlari)
delta_g = req_sc - Total_Sc

st.write(f"**TLARI Score for {selected_ai}:** {tlari} | **Required Capacity:** {req_sc:.4f}")

if delta_g > 0:
    st.error(f"🚨 **Governance Deficit ($\Delta G$): {delta_g:.4f}** (Calculated as Required - Sc. System complexity exceeds capacity.)")
else:
    st.success(f"🛡️ **Surplus Capacity:** {abs(delta_g):.4f} (The institution can safely govern this AI)")

# --- NEW: ELEVATING ENHANCEMENTS (STRESS TEST & CSV) ---
st.markdown("---")
st.subheader("3. Stochastic Stress Test (Monte Carlo)")
st.markdown(f"Run 1,000 rapid Monte Carlo iterations centered around your current slider positions to visualize the **Non-Substitution Theorem** and calculate the real-time failure rate against the **{selected_ai}**.")

if st.button("🚀 Run 1,000 Iteration Stress Test"):
    with st.spinner('Generating 1,000 stochastic universes...'):
        # Dynamic Beta Distribution Generator (using sliders as means)
        nu = 15 # Variance control
        def gen_beta(mean_val, n=1000):
            mu = np.clip(mean_val, 0.05, 0.95)
            return np.random.beta(mu * nu, (1 - mu) * nu, n)

        sim_hol = gen_beta(HOL)
        sim_l = gen_beta(L)
        sim_eth = gen_beta(Eth)
        sim_gov = gen_beta(Gov)
        sim_reg = gen_beta(Reg)

        # Apply Mathematical Framework to Arrays
        sim_fhol = 1.0 / (1.0 + np.exp(-k * (sim_hol - h0)))
        sim_sc = sim_fhol * (sim_l**0.70) * (sim_eth**1.20) * (sim_gov**0.80) * (sim_reg**0.90)

        # Build DataFrame
        df_sim = pd.DataFrame({
            'HOL': sim_hol, 'L': sim_l, 'Eth': sim_eth, 'Gov': sim_gov, 'Reg': sim_reg, 
            'Barrier (f_HOL)': sim_fhol, 'Total Sc': sim_sc
        })
        df_sim['Status'] = np.where(df_sim['Total Sc'] < req_sc, 'DEFICIT', 'SAFE')

        # Calculate Failure Rate
        failure_rate = (df_sim['Status'] == 'DEFICIT').mean() * 100

        # Display Results
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("Stress Test Mean Sc", f"{sim_sc.mean():.4f}")
        col_res2.metric("System Failure Rate", f"{failure_rate:.1f}%", delta_color="inverse")

        if failure_rate > 50:
            st.error("🚨 **CRITICAL VULNERABILITY:** The systemic variance causes the environment to collapse under stress.")
        else:
            st.success("🛡️ **SYSTEM RESILIENT:** The institutional architecture successfully absorbs variance.")

        # Plot Histogram
        st.write("**Stochastic Distribution of Total Capacity (Sc)**")
        st.bar_chart(np.histogram(sim_sc, bins=30)[0])

        # Export to CSV Button
        csv = df_sim.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Raw Simulation Data (CSV)",
            data=csv,
            file_name='ASCF_Stress_Test_Results.csv',
            mime='text/csv',
        )

# Official Citation Panel
st.markdown("---")
st.caption("ASCF Dashboard v2.0 | Salihu, H. (2026). Algorithmic Stewardship Competency Framework, Tarrant County College District | MC seed=20260307 | Parameters: α=0.70, βe=1.20, γg=0.80, δr=0.90, λ=0.50")