import streamlit as st
import pandas as pd
import plotly.express as px
from styles import apply_theme
from engine import run_capital_rationing

st.set_page_config(page_title="Strategic Capital Allocator", layout="wide")
apply_theme()

# --- Sidebar Navigation (Logical Steps) ---
st.sidebar.title("Decision Workflow")
step = st.sidebar.radio("Navigate Process", [
    "1. Decision Context",
    "2. Financial Evaluation",
    "3. Forward-Looking Analysis",
    "4. Capital Trade-offs",
    "5. Uncertainty & Scenarios",
    "6. Decision Summary",
    "7. AI Interpretation"
])

# --- Shared Data State ---
if 'projects' not in st.session_state:
    st.session_state.projects = pd.DataFrame([
        {"Project": "Expansion A", "Investment": 500, "NPV": 150, "Risk": "Low"},
        {"Project": "R&D Alpha", "Investment": 300, "NPV": 200, "Risk": "High"},
        {"Project": "IT Modernization", "Investment": 200, "NPV": 50, "Risk": "Med"}
    ])

# --- Step 1: Decision Context ---
if step == "1. Decision Context":
    st.markdown('<p class="step-header">Phase 1</p>', unsafe_allow_html=True)
    st.title("Strategic Framing")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Business Context")
        st.text_area("Investment Objective", "Allocate surplus capital for FY2026 growth initiatives.")
        horizon = st.selectbox("Investment Horizon", ["3 Years", "5 Years", "10 Years"])
    with col2:
        st.subheader("Constraint Framing")
        total_budget = st.number_input("Total Capital Available ($M)", value=1000)
        risk_appetite = st.select_slider("Risk Tolerance", ["Conservative", "Moderate", "Aggressive"])

# --- Step 2: Project Financial Evaluation ---
elif step == "2. Financial Evaluation":
    st.title("Fundamental Analysis")
    st.write("Finance-first screening of individual project merits.")
    st.data_editor(st.session_state.projects, use_container_width=True)
    
    # NPV/IRR Logic visualization
    st.info("📌 Signals: Evaluation based on Cash-Flow Volatility and Payback, not just ROI.")

# --- Step 4: Capital Trade-offs (Your Signature Section) ---
elif step == "4. Capital Trade-offs":
    st.title("Capital Rationing & Priority")
    budget = st.slider("Adjust Budget Constraint", 100, 2000, 700)
    
    results, spent = run_capital_rationing(st.session_state.projects, budget)
    
    st.subheader(f"Portfolio Results (${spent}M / ${budget}M Utilized)")
    st.table(results[['Project', 'Investment', 'NPV', 'PI', 'Status']])
    
    # Trade-off Visualization
    fig = px.bar(results, x="Project", y="NPV", color="Status", 
                 title="The Cost of Scarcity: Funded vs. Deferred Projects")
    st.plotly_chart(fig)

# --- Step 6: Decision Summary ---
elif step == "6. Decision Summary":
    st.title("Investment Committee Readiness")
    st.markdown("""
    ### Final Recommendation Log
    - **Total Allocation:** Approved projects represent 85% of risk budget.
    - **Key Rationale:** Prioritized high PI projects over high absolute NPV to maximize capital efficiency.
    - **Risk Flags:** R&D Alpha is highly sensitive to WACC fluctuations.
    """)
    if st.button("Generate Governance Memo"):
        st.success("Memo exported for Investment Committee review.")

# --- Step 7: AI Interpretation Assistant ---
elif step == "7. AI Interpretation":
    st.title("Analytical Support")
    st.chat_input("Ask about the logic (e.g., 'Why was Project B deferred?')")
    st.markdown("> **Note:** This assistant explains calculations and clarifies assumptions; it does not provide autonomous advice.")
