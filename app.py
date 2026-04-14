import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

# Title and Academic Context
st.set_page_config(page_title="ASCF Dashboard v3.0", layout="wide")
st.title("Algorithmic Stewardship Capacity (ASCF) Dashboard")
st.markdown("Interactive Systemic Risk, Governance Deficit ($\Delta G$), and Theoretical Visualizations")

# Sidebar for 5-Pillar Inputs
st.sidebar.header("Institutional Parameters (Inputs)")
st.sidebar.markdown("Adjust these sliders to set the baseline environment.")
HOL = st.sidebar.slider("Human-in-the-Loop (HOL)", 0.0, 1.0, 0.75)
L   = st.sidebar.slider("Algorithmic Literacy (L)", 0.0, 1.0, 0.71)
Eth = st.sidebar.slider("Ethical Cohesion (Eth)", 0.0, 1.0, 0.80)
Gov = st.sidebar.slider("Institutional Governance (Gov)", 0.0, 1.0, 0.77)
Reg = st.sidebar.slider("Regulatory Enforcement (Reg)", 0.0, 1.0, 0.80)

# ASCF Mathematical Engine (Deterministic)
k = 10.0
h0 = 0.55
alpha = 0.70
beta = 1.20
gamma = 0.85
lam = 0.50

f_HOL = 1.0 / (1.0 + np.exp(-k * (HOL - h0)))
Total_Sc = f_HOL * (L**alpha) * (Eth**beta) * (Gov**gamma) * (Reg**0.90)

# Create 3 Professional Tabs for the Committee
tab1, tab2, tab3 = st.tabs(["📊 Core Calculator", "🚀 Stochastic Stress Test", "📈 Theoretical Visualizations"])

# ==========================================
# TAB 1: CORE CALCULATOR
# ==========================================
with tab1:
    st.subheader("1. Static Systemic Capacity Output")
    col1, col2 = st.columns(2)
    col1.metric(label="Barrier of Agency (f_HOL)", value=f"{f_HOL:.4f}")
    col2.metric(label="Total Stewardship Capacity (Sc)", value=f"{Total_Sc:.4f}")

    if Total_Sc < 0.10:
        st.error("⚠️ SYSTEM DEFICIT: Structural capacity is near-zero due to weak-link failure.")
    else:
        st.success("✅ SYSTEM STABLE: Institutional structures are supporting human oversight.")

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
    req_sc = lam * np.log(tlari)
    delta_g = req_sc - Total_Sc

    st.write(f"**TLARI Score for {selected_ai}:** {tlari} | **Required Capacity:** {req_sc:.4f}")

    if delta_g > 0:
        st.error(f"🚨 **Governance Deficit ($\Delta G$): {delta_g:.4f}** (System complexity exceeds capacity.)")
    else:
        st.success(f"🛡️ **Surplus Capacity:** {abs(delta_g):.4f} (Institution can safely govern this AI)")

# ==========================================
# TAB 2: STRESS TEST
# ==========================================
with tab2:
    st.subheader("Stochastic Stress Test (Monte Carlo)")
    st.markdown("Run 1,000 rapid Monte Carlo iterations centered around your current slider positions.")

    if st.button("🚀 Run 1,000 Iteration Stress Test"):
        with st.spinner('Generating stochastic universes...'):
            nu = 15 
            def gen_beta(mean_val, n=1000):
                mu = np.clip(mean_val, 0.05, 0.95)
                return np.random.beta(mu * nu, (1 - mu) * nu, n)

            sim_hol, sim_l, sim_eth, sim_gov, sim_reg = gen_beta(HOL), gen_beta(L), gen_beta(Eth), gen_beta(Gov), gen_beta(Reg)
            sim_fhol = 1.0 / (1.0 + np.exp(-k * (sim_hol - h0)))
            sim_sc = sim_fhol * (sim_l**alpha) * (sim_eth**beta) * (sim_gov**gamma) * (sim_reg**0.90)

            df_sim = pd.DataFrame({'HOL': sim_hol, 'L': sim_l, 'Eth': sim_eth, 'Gov': sim_gov, 'Reg': sim_reg, 'Sc': sim_sc})
            df_sim['Status'] = np.where(df_sim['Sc'] < req_sc, 'DEFICIT', 'SAFE')
            failure_rate = (df_sim['Status'] == 'DEFICIT').mean() * 100

            col_res1, col_res2 = st.columns(2)
            col_res1.metric("Stress Test Mean Sc", f"{sim_sc.mean():.4f}")
            col_res2.metric("System Failure Rate", f"{failure_rate:.1f}%", delta_color="inverse")

            st.bar_chart(np.histogram(sim_sc, bins=30)[0])
            st.download_button("📥 Download Raw Simulation Data (CSV)", data=df_sim.to_csv(index=False).encode('utf-8'), file_name='ASCF_Stress_Test.csv', mime='text/csv')

# ==========================================
# TAB 3: THEORETICAL VISUALIZATIONS
# ==========================================
with tab3:
    st.subheader("ASCF Mathematical Architecture")
    st.markdown("Dynamic rendering of canonical framework charts.")
    sns.set_theme(style="whitegrid")

    colA, colB = st.columns(2)

    with colA:
        # Figure 1.7
        fig7, ax7 = plt.subplots(figsize=(6, 4))
        hol_range = np.linspace(0, 1, 100)
        act = 1 / (1 + np.exp(-k * (hol_range - h0)))
        ax7.plot(hol_range, act, color='black', lw=3)
        ax7.axvspan(0, h0, color='pink', alpha=0.3, label=f'Operator Zone (< {h0})')
        ax7.axvspan(h0, 1.0, color='lightblue', alpha=0.3, label=f'Steward Zone (>= {h0})')
        ax7.set_title('Fig 1.7: Barrier of Agency Sigmoid')
        ax7.legend()
        st.pyplot(fig7)

        # Figure 1.6
        fig6, ax6 = plt.subplots(figsize=(6, 4))
        x_vals = np.linspace(0, 1, 100)
        ax6.plot(x_vals, x_vals**beta, label='Ethics (Exp)', color='#000080', lw=2)
        ax6.plot(x_vals, x_vals**gamma, label='Gov (Dim)', color='#1f77b4', lw=2, linestyle='--')
        ax6.plot(x_vals, x_vals**alpha, label='Lit (Dim)', color='#2ca02c', lw=2, linestyle='-.')
        ax6.set_title('Fig 1.6: Domain Sensitivity')
        ax6.legend()
        st.pyplot(fig6)

    with colB:
        # Figure 1.5 (Isoquant)
        fig5, ax5 = plt.subplots(figsize=(6, 4))
        L_grid, E_grid = np.meshgrid(np.linspace(0.01, 1, 50), np.linspace(0.01, 1, 50))
        Sc_grid = f_HOL * (L_grid**alpha) * (E_grid**beta) * (Gov**gamma)
        contour = ax5.contourf(L_grid, E_grid, Sc_grid, levels=15, cmap='viridis')
        fig5.colorbar(contour)
        ax5.set_title('Fig 1.5: Dynamic Sc Isoquant Map')
        ax5.set_xlabel('Literacy (L)'); ax5.set_ylabel('Ethics (Eth)')
        st.pyplot(fig5)

        # Figure 1.2 Panel A
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        cases = ['COMPAS', 'SyRI', 'Watson', 'ABE Robo', 'Amazon HRT', 'SEC PDA']
        deltas = [1.436, 1.328, 1.021, 1.020, 0.798, 0.723]
        sns.barplot(x=deltas, y=cases, ax=ax2, hue=cases, palette='Reds_r', legend=False)
        ax2.set_title('Fig 1.2: Canonical Deficits (ΔG)')
        st.pyplot(fig2)

    st.markdown("---")
    # Figure 1.8 3D Surface
    st.markdown("**Figure 1.8: Systemic Capacity 3D Architecture**")
    fig8 = plt.figure(figsize=(8, 6))
    ax8 = fig8.add_subplot(111, projection='3d')
    surf = ax8.plot_surface(L_grid, E_grid, Sc_grid, cmap='magma', edgecolor='none', alpha=0.9)
    ax8.set_xlabel('Literacy'); ax8.set_ylabel('Ethics'); ax8.set_zlabel('Stewardship Capacity (Sc)')
    fig8.colorbar(surf, shrink=0.5, aspect=10, pad=0.1)
    st.pyplot(fig8)

# Official Citation Panel
st.markdown("---")
st.caption("ASCF Dashboard v3.0 | Salihu, H. (2026). Algorithmic Stewardship Competency Framework, Tarrant County College District | MC seed=20260307")