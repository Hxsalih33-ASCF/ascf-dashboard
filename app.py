import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

# ==========================================
# GLOBAL PUBLICATION STYLE GUIDE
# ==========================================
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titleweight': 'bold',
    'axes.edgecolor': '#333333',
    'axes.linewidth': 1.5,
    'grid.color': '#E0E0E0',
    'grid.linestyle': '--',
    'figure.facecolor': 'white'
})

C_NAVY, C_BLUE, C_LIGHTBLUE = '#1D3557', '#457B9D', '#A8DADC'
C_RED, C_PINK, C_GREEN = '#E63946', '#FAD2E1', '#2A9D8F'

# ==========================================
# DASHBOARD SETUP & MATH ENGINE
# ==========================================
st.set_page_config(page_title="ASCF Dashboard v4.0", layout="wide")
st.title("Algorithmic Stewardship Capacity (ASCF) Dashboard")
st.markdown("Interactive Systemic Risk, Governance Deficit ($\Delta G$), and Stochastic Stress Testing")

st.sidebar.header("Institutional Parameters (Inputs)")
st.sidebar.markdown("Adjust these sliders to set the baseline environment.")
HOL = st.sidebar.slider("Human-in-the-Loop (HOL)", 0.0, 1.0, 0.75)
L   = st.sidebar.slider("Algorithmic Literacy (L)", 0.0, 1.0, 0.71)
Eth = st.sidebar.slider("Ethical Cohesion (Eth)", 0.0, 1.0, 0.80)
Gov = st.sidebar.slider("Institutional Governance (Gov)", 0.0, 1.0, 0.77)
Reg = st.sidebar.slider("Regulatory Enforcement (Reg)", 0.0, 1.0, 0.80)

k, h0, alpha, beta, gamma, lam = 10.0, 0.55, 0.70, 1.20, 0.85, 0.50

f_HOL = 1.0 / (1.0 + np.exp(-k * (HOL - h0)))
Total_Sc = f_HOL * (L**alpha) * (Eth**beta) * (Gov**gamma) * (Reg**0.90)

tab1, tab2, tab3 = st.tabs(["📊 Core Calculator", "🚀 Stochastic Stress Test", "📈 Theoretical Visualizations"])

# ==========================================
# TAB 1: CORE CALCULATOR
# ==========================================
with tab1:
    st.subheader("1. Static Systemic Capacity Output")
    col1, col2 = st.columns(2)
    col1.metric(label="Barrier of Agency (f_HOL)", value=f"{f_HOL:.4f}")
    col2.metric(label="Total Stewardship Capacity (Sc)", value=f"{Total_Sc:.4f}")

    if Total_Sc < 0.10: st.error("⚠️ SYSTEM DEFICIT: Structural capacity is near-zero due to weak-link failure.")
    else: st.success("✅ SYSTEM STABLE: Institutional structures are supporting human oversight.")

    st.subheader("2. Governance Deficit Matrix ($\Delta G$)")
    ai_systems = {"National Biometric ID": 16.50, "COMPAS (Recidivism)": 14.31, "SyRI (Welfare Fraud)": 11.59,
                  "Automated Tax Auditing": 11.59, "Predictive Credit Scoring": 9.20, "IBM Watson Health": 8.76,
                  "Amazon HR Tool": 7.16, "Generative LLM (SEC)": 5.70}

    selected_ai = st.selectbox("Select AI System to Deploy:", list(ai_systems.keys()))
    tlari = ai_systems[selected_ai]
    req_sc = lam * np.log(tlari)
    delta_g = req_sc - Total_Sc

    st.write(f"**TLARI Score:** {tlari} | **Required Capacity:** {req_sc:.4f}")

    if delta_g > 0: st.error(f"🚨 **Governance Deficit ($\Delta G$): {delta_g:.4f}** (System complexity exceeds capacity.)")
    else: st.success(f"🛡️ **Surplus Capacity:** {abs(delta_g):.4f} (Institution can safely govern this AI)")

# ==========================================
# TAB 2: STRESS TEST (Now with P5 and P95!)
# ==========================================
with tab2:
    st.subheader("Stochastic Stress Test (Monte Carlo)")
    st.markdown("Run 1,000 Monte Carlo iterations centered around your current slider positions. Evaluates tail risks (P5/P95).")

    if st.button("🚀 Run 1,000 Iteration Stress Test"):
        with st.spinner('Generating stochastic universes...'):
            nu = 15 
            def gen_beta(mean_val, n=1000):
                mu = np.clip(mean_val, 0.05, 0.95)
                return np.random.beta(mu * nu, (1 - mu) * nu, n)

            sim_hol, sim_l, sim_eth, sim_gov, sim_reg = gen_beta(HOL), gen_beta(L), gen_beta(Eth), gen_beta(Gov), gen_beta(Reg)
            sim_fhol = 1.0 / (1.0 + np.exp(-k * (sim_hol - h0)))
            sim_sc = sim_fhol * (sim_l**alpha) * (sim_eth**beta) * (sim_gov**gamma) * (sim_reg**0.90)

            failure_rate = (sim_sc < req_sc).mean() * 100
            
            # Statistical Tail Extraction
            p5, p95 = np.percentile(sim_sc, 5), np.percentile(sim_sc, 95)

            col_res1, col_res2, col_res3, col_res4 = st.columns(4)
            col_res1.metric("Mean Sc", f"{sim_sc.mean():.4f}")
            col_res2.metric("Failure Rate", f"{failure_rate:.1f}%", delta_color="inverse")
            col_res3.metric("P5 (Worst-Case)", f"{p5:.4f}")
            col_res4.metric("P95 (Best-Case)", f"{p95:.4f}")

            # Styled Histogram
            fig_hist, ax_hist = plt.subplots(figsize=(10, 4))
            sns.histplot(sim_sc, bins=30, color=C_BLUE, kde=True, ax=ax_hist)
            ax_hist.axvline(req_sc, color=C_RED, ls='--', lw=2, label=f'Required ({req_sc:.2f})')
            ax_hist.set_title("Stochastic Distribution of Capacity")
            ax_hist.legend()
            st.pyplot(fig_hist)

# ==========================================
# TAB 3: THEORETICAL VISUALIZATIONS (Styled)
# ==========================================
with tab3:
    st.subheader("ASCF Mathematical Architecture")
    colA, colB = st.columns(2)

    with colA:
        # Styled Figure 1.7
        fig7, ax7 = plt.subplots(figsize=(6, 4))
        hol_range = np.linspace(0, 1, 100)
        act = 1 / (1 + np.exp(-k * (hol_range - h0)))
        ax7.plot(hol_range, act, color=C_NAVY, lw=3, zorder=3)
        ax7.axvspan(0, h0, color=C_PINK, alpha=0.5, zorder=1)
        ax7.axvspan(h0, 1.0, color=C_LIGHTBLUE, alpha=0.4, zorder=1)
        ax7.axvline(h0, color=C_RED, ls=':', lw=2)
        ax7.text(0.25, 0.8, 'OPERATOR ZONE', ha='center', color='#780000', fontweight='bold', bbox=dict(facecolor='white', edgecolor=C_PINK, boxstyle='round,pad=0.3'), zorder=4)
        ax7.text(0.80, 0.2, 'STEWARD ZONE', ha='center', color=C_NAVY, fontweight='bold', bbox=dict(facecolor='white', edgecolor=C_LIGHTBLUE, boxstyle='round,pad=0.3'), zorder=4)
        ax7.set_title('Fig 1.7: Barrier of Agency Sigmoid')
        st.pyplot(fig7)

        # Styled Figure 1.6
        fig6, ax6 = plt.subplots(figsize=(6, 4))
        x_vals = np.linspace(0, 1, 100)
        ax6.plot(x_vals, x_vals**beta, label='Ethics (Exp)', color=C_NAVY, lw=3)
        ax6.plot(x_vals, x_vals**gamma, label='Gov (Dim)', color=C_BLUE, lw=3, ls='--')
        ax6.plot(x_vals, x_vals**alpha, label='Lit (Dim)', color=C_GREEN, lw=3, ls='-.')
        ax6.axvspan(0, h0, color='#E0E0E0', alpha=0.5)
        ax6.set_title('Fig 1.6: Domain Sensitivity')
        ax6.legend()
        st.pyplot(fig6)

    with colB:
        # Styled Figure 1.5
        fig5, ax5 = plt.subplots(figsize=(6, 4))
        L_grid, E_grid = np.meshgrid(np.linspace(0.01, 1, 50), np.linspace(0.01, 1, 50))
        Sc_grid = f_HOL * (L_grid**alpha) * (E_grid**beta) * (Gov**gamma)
        contour = ax5.contourf(L_grid, E_grid, Sc_grid, levels=15, cmap='YlGnBu')
        fig5.colorbar(contour)
        ax5.set_title('Fig 1.5: Dynamic Sc Isoquant Map')
        ax5.set_xlabel('Literacy (L)'); ax5.set_ylabel('Ethics (Eth)')
        st.pyplot(fig5)

        # Styled Figure 1.2 Panel A
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        cases, deltas = ['COMPAS', 'SyRI', 'Watson', 'ABE Robo', 'Amazon', 'SEC PDA'], [1.436, 1.328, 1.021, 1.020, 0.798, 0.723]
        sns.barplot(x=deltas, y=cases, ax=ax2, hue=cases, palette='rocket', legend=False)
        ax2.set_title('Fig 1.2: Canonical Deficits ($\Delta G$)')
        st.pyplot(fig2)

st.markdown("---")
st.caption("ASCF Dashboard v4.0 (Defense Edition) | Salihu, H. (2026). Algorithmic Stewardship Competency Framework | MC seed=20260307")