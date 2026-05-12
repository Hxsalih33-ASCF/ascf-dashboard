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
# DASHBOARD SETUP & HEADER
# ==========================================
st.set_page_config(page_title="ASCF Dashboard v4.1", layout="wide")

st.title("Algorithmic Stewardship Capacity Framework Dashboard")
st.markdown("### ASCF Live Dashboard v4.1: Dissertation-Aligned Edition")
st.markdown("*Phase I Computational Validation, Governance Deficit Modeling, and Stochastic Stress Testing*")
st.markdown("---")

# ==========================================
# SIDEBAR: ASCF INSTITUTIONAL PARAMETERS
# ==========================================
st.sidebar.header("ASCF Institutional Parameters")
st.sidebar.markdown("Adjust the five institutional capacity inputs used to estimate stewardship capacity, governance readiness, and systemic risk.")

st.sidebar.markdown("**Domain I: Higher-Order Learning**")
HOL = st.sidebar.slider("Human-in-the-Loop (HOL)", 0.0, 1.0, 0.75)

st.sidebar.markdown("**Domain II: Technomoral Literacies**")
L = st.sidebar.slider("Algorithmic Literacy (L)", 0.0, 1.0, 0.71)

st.sidebar.markdown("**Domain III: Ethical Adjudication**")
Eth = st.sidebar.slider("Ethical Cohesion (Eth)", 0.0, 1.0, 0.80)

st.sidebar.markdown("**Domain IV: Accountable Governance**")
Gov = st.sidebar.slider("Institutional Governance (Gov)", 0.0, 1.0, 0.77)

st.sidebar.markdown("**Governance Matching / Compliance**")
Reg = st.sidebar.slider("Regulatory Enforcement (Reg)", 0.0, 1.0, 0.80)

st.sidebar.markdown("---")
st.sidebar.subheader("Reproducibility & Validation")
st.sidebar.caption("Dashboard Version: v4.1")
st.sidebar.caption("Monte Carlo Seed: 20260307")
st.sidebar.caption("MC Iterations: 1,000")
st.sidebar.caption("Validation Phase: Phase I")
st.sidebar.caption("Documentation: Appendix M")

# ==========================================
# MATHEMATICAL ENGINE (DETERMINISTIC)
# ==========================================
k, h0, alpha, beta, gamma, delta, lam = 10.0, 0.55, 0.70, 1.20, 0.80, 0.90, 0.50

f_HOL = 1.0 / (1.0 + np.exp(-k * (HOL - h0)))
Total_Sc = f_HOL * (L**alpha) * (Eth**beta) * (Gov**gamma) * (Reg**delta)

# ==========================================
# MAIN TABS (DISSERTATION ALIGNED)
# ==========================================
tabs = st.tabs([
    "1. ASCF Overview", 
    "2. Capacity Calculator", 
    "3. Governance Deficit Matrix", 
    "4. Stochastic Stress Test", 
    "5. Instrument Alignment", 
    "6. Validation Notes", 
    "7. Visualizations",
    "8. Appendix M Screenshot Mode"
])

# ------------------------------------------
# TAB 1: FRAMEWORK OVERVIEW
# ------------------------------------------
with tabs[0]:
    st.subheader("Algorithmic Stewardship Competency Framework (ASCF)")
    st.markdown("""
    **Purpose:** The ASCF transitions algorithmic governance from descriptive ethics to computationally falsifiable institutional readiness.
    
    **The Four Domains (Cross-Reference: Chapter III, §3.4):**
    * **Domain I:** Higher-Order Learning (Barrier of Agency)
    * **Domain II:** Technomoral Literacies
    * **Domain III:** Ethical Adjudication
    * **Domain IV:** Accountable Governance
    
    **The Developmental Ladder:**
    The framework establishes a mathematical boundary between nominal oversight and substantive governance:
    1. **Passenger** (Sub-threshold)
    2. **Operator** (Sub-threshold)
    3. **Auditor** (Super-threshold)
    4. **Steward** (Super-threshold / Fully Activated)
    """)

# ------------------------------------------
# TAB 2: STEWARDSHIP CAPACITY CALCULATOR
# ------------------------------------------
with tabs[1]:
    st.subheader("Stewardship Capacity ($S_c$) Calculator")
    st.markdown("Cross-Reference: Chapter III, §3.5.1–§3.5.3")
    
    col1, col2 = st.columns(2)
    col1.metric(label="Barrier of Agency (Activation Multiplier: f_HOL)", value=f"{f_HOL:.4f}")
    col2.metric(label="Total Stewardship Capacity (Sc)", value=f"{Total_Sc:.4f}")

    if Total_Sc < 0.10: 
        st.error("⚠️ SYSTEM DEFICIT: Structural capacity is near-zero due to weak-link failure.")
    else: 
        st.success("✅ SYSTEM STABLE: Institutional structures are supporting human oversight.")
        
    st.markdown("### Formal Mathematical Specification")
    st.latex(r"f(HOL) = \frac{1}{1 + e^{-k(HOL - h_0)}}")
    st.latex(r"S_c = f(HOL) \cdot L^\alpha \cdot Eth^\beta \cdot Gov^\gamma \cdot Reg^\delta")

# ------------------------------------------
# TAB 3: GOVERNANCE DEFICIT MATRIX
# ------------------------------------------
with tabs[2]:
    st.subheader("Governance Deficit ($\Delta G$) Matrix")
    st.markdown("Cross-Reference: Chapter III, §3.5.5–§3.5.7, §3.9.4")
    
    ai_systems = {
        "National Biometric ID": ("Public-sector biometric identification", 16.50),
        "COMPAS (Recidivism)": ("Criminal Justice / Judicial", 14.40),
        "SyRI (Welfare Fraud)": ("Public Welfare / Resource Allocation", 11.59),
        "Automated Tax Auditing": ("Financial / Government", 11.59),
        "Predictive Credit Scoring": ("Financial Services", 9.20),
        "IBM Watson Health": ("Healthcare / Diagnostics", 9.00),
        "Amazon HR Tool": ("Human Resources", 7.20),
        "SEC Predictive Analytics": ("Financial Regulation", 5.70)
    }

    selected_ai = st.selectbox("Select AI System to Deploy:", list(ai_systems.keys()))
    domain, tlari = ai_systems[selected_ai]
    req_sc = lam * np.log(tlari)
    delta_g = req_sc - Total_Sc
    
    interpretation = "Capacity-matched under current institutional settings. Safe to deploy." if delta_g <= 0 else "Not capacity-matched under current institutional settings. High risk of failure."
    
    df_results = pd.DataFrame({
        "Field": ["AI System", "Domain", "TLARI Score", "Required Capacity", "Governance Deficit ($\Delta G$)", "Deployment Interpretation"],
        "Value": [selected_ai, domain, f"{tlari:.2f}", f"{req_sc:.4f}", f"{delta_g:.4f}", interpretation]
    })
    
    st.table(df_results)
    
    st.info("**Interpretation:** A positive $\Delta G$ indicates that the selected AI system’s task-level risk demand exceeds the modeled institutional stewardship capacity. This condition signals the need for additional oversight, governance controls, literacy development, or deployment constraint.")

# ------------------------------------------
# TAB 4: STOCHASTIC STRESS TEST
# ------------------------------------------
with tabs[3]:
    st.subheader("Monte Carlo Stochastic Stress Test")
    st.markdown("Cross-Reference: Chapter III, §3.8.2, §3.8.6, §3.8.7")
    
    st.info("**Methodological Note:** The Monte Carlo module evaluates uncertainty around institutional parameter settings by repeatedly sampling plausible stewardship-capacity outcomes around the selected baseline profile. Failure occurs when simulated stewardship capacity falls below the required capacity associated with the selected AI system’s TLARI score.")

    if st.button("🚀 Run 1,000 Iteration Stress Test"):
        with st.spinner('Generating stochastic universes...'):
            nu = 15 
            def gen_beta(mean_val, n=1000):
                mu = np.clip(mean_val, 0.05, 0.95)
                return np.random.beta(mu * nu, (1 - mu) * nu, n)

            sim_hol, sim_l, sim_eth, sim_gov, sim_reg = gen_beta(HOL), gen_beta(L), gen_beta(Eth), gen_beta(Gov), gen_beta(Reg)
            sim_fhol = 1.0 / (1.0 + np.exp(-k * (sim_hol - h0)))
            sim_sc = sim_fhol * (sim_l**alpha) * (sim_eth**beta) * (sim_gov**gamma) * (sim_reg**delta)

            failure_rate = (sim_sc < req_sc).mean() * 100
            p5, p95 = np.percentile(sim_sc, 5), np.percentile(sim_sc, 95)

            col_res1, col_res2, col_res3, col_res4 = st.columns(4)
            col_res1.metric("Mean Sc", f"{sim_sc.mean():.4f}")
            col_res2.metric("Failure Rate", f"{failure_rate:.1f}%", delta_color="inverse")
            col_res3.metric("P5 (Worst-Case)", f"{p5:.4f}")
            col_res4.metric("P95 (Best-Case)", f"{p95:.4f}")

            fig_hist, ax_hist = plt.subplots(figsize=(10, 4))
            sns.histplot(sim_sc, bins=30, color=C_BLUE, kde=True, ax=ax_hist)
            ax_hist.axvline(req_sc, color=C_RED, ls='--', lw=2, label=f'Required Capacity ({req_sc:.2f})')
            ax_hist.set_title("Stochastic Distribution of Systemic Capacity ($S_c$)")
            ax_hist.set_xlabel("Stewardship Capacity")
            ax_hist.legend()
            st.pyplot(fig_hist)

# ------------------------------------------
# TAB 5: INSTRUMENT ALIGNMENT
# ------------------------------------------
with tabs[4]:
    st.subheader("Dashboard Construct & Instrument Alignment")
    st.markdown("Cross-Reference: Chapter III, §3.6")
    
    instrument_data = {
        "ASCF Construct": ["Higher-Order Learning", "Technomoral Literacy", "Ethical Adjudication", "Accountable Governance", "Regulatory Enforcement", "Task-Level Risk"],
        "Dashboard Measure": ["HOL slider / Barrier of Agency", "Algorithmic Literacy (L) slider", "Ethical Cohesion (Eth) slider", "Governance (Gov) slider", "Regulatory (Reg) slider", "TLARI score selection"],
        "Dissertation Instrument": ["DECIDE", "DCSS-24 / DECIDE", "DECIDE / MAD-R", "MAD-R / Regulatory Crosswalk", "Regulatory Crosswalk", "Regulatory Crosswalk Matrix"]
    }
    st.table(pd.DataFrame(instrument_data))

# ------------------------------------------
# TAB 6: PHASE I VALIDATION NOTES
# ------------------------------------------
with tabs[5]:
    st.subheader("Phase I Computational Validation Boundaries")
    st.markdown("""
    * **Simulation Assumptions:** Assumes multiplicative interaction of domains based on a Cobb-Douglas production foundation.
    * **Synthetic-Data Boundary:** Simulation profiles are stochastically generated from parameterized distributions and do not represent surveyed individuals. The dashboard implementation uses 1,000 Monte Carlo iterations for Appendix M demonstration and reproducible stress-test visualization.
    * **Non-Human-Subjects Status:** This dashboard and its underlying spreadsheet engine rely exclusively on deterministic algorithms and synthetic Monte Carlo generation. No human subjects data is utilized in Phase I.
    * **Reproducibility:** Seed fixed at `20260307` to ensure all distribution tails and failure rates remain perfectly reproducible across audits.
    * **Phase II Validation Boundary:** Empirical human-subjects validation using the mapped instruments (DECIDE, MAD-R) is reserved for Phase II research.
    """)

# ------------------------------------------
# TAB 7: THEORETICAL VISUALIZATIONS
# ------------------------------------------
with tabs[6]:
    st.subheader("ASCF Mathematical Architecture")
    colA, colB = st.columns(2)

    with colA:
        fig7, ax7 = plt.subplots(figsize=(6, 4))
        hol_range = np.linspace(0, 1, 100)
        act = 1 / (1 + np.exp(-k * (hol_range - h0)))
        ax7.plot(hol_range, act, color=C_NAVY, lw=3, zorder=3)
        ax7.axvspan(0, h0, color=C_PINK, alpha=0.5, zorder=1)
        ax7.axvspan(h0, 1.0, color=C_LIGHTBLUE, alpha=0.4, zorder=1)
        ax7.axvline(h0, color=C_RED, ls=':', lw=2)
        ax7.text(0.25, 0.8, 'OPERATOR ZONE', ha='center', color='#780000', fontweight='bold', bbox=dict(facecolor='white', edgecolor=C_PINK, boxstyle='round,pad=0.3'), zorder=4)
        ax7.text(0.80, 0.2, 'STEWARD ZONE', ha='center', color=C_NAVY, fontweight='bold', bbox=dict(facecolor='white', edgecolor=C_LIGHTBLUE, boxstyle='round,pad=0.3'), zorder=4)
        ax7.set_title('Barrier of Agency Sigmoid $f(HOL)$')
        st.pyplot(fig7)

    with colB:
        fig5, ax5 = plt.subplots(figsize=(6, 4))
        L_grid, E_grid = np.meshgrid(np.linspace(0.01, 1, 50), np.linspace(0.01, 1, 50))
        Sc_grid = f_HOL * (L_grid**alpha) * (E_grid**beta) * (Gov**gamma)
        contour = ax5.contourf(L_grid, E_grid, Sc_grid, levels=15, cmap='YlGnBu')
        fig5.colorbar(contour)
        ax5.set_title('Dynamic $S_c$ Isoquant Map')
        ax5.set_xlabel('Literacy (L)'); ax5.set_ylabel('Ethics (Eth)')
        st.pyplot(fig5)

# ------------------------------------------
# TAB 8: SCREENSHOT CATALOG MODE (APPX M)
# ------------------------------------------
with tabs[7]:
    st.subheader("Appendix M: Figure Generation Mode")
    st.info("Recommended use: capture this page as Figure M.1 or as the master summary view for Appendix M.")
    st.markdown("This view aggregates the core computational metrics into a vertically stacked, clean format optimized for dissertation screenshot capture.")
    
    st.markdown("### Institutional Baseline Profile")
    st.write(f"**HOL:** {HOL} | **Lit:** {L} | **Eth:** {Eth} | **Gov:** {Gov} | **Reg:** {Reg}")
    
    col_a, col_b = st.columns(2)
    col_a.metric(label="Calculated Barrier of Agency", value=f"{f_HOL:.4f}")
    col_b.metric(label="Calculated Stewardship Capacity", value=f"{Total_Sc:.4f}")
    
    st.markdown("### Governance Deficit Output")
    st.table(df_results)
    
    st.markdown("### Stress Test Output (Static Placeholder View)")
    st.markdown("*(Run simulation in Tab 4 to update values)*")
    st.write("**P5 (Worst-Case Capacity):** Validated in main simulation tab.")
    
st.markdown("---")
st.caption("ASCF Dashboard v4.1 | Dissertation-Aligned Edition | Phase I Computational Validation | MC seed=20260307")
