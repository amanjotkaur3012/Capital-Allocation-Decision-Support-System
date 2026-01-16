import streamlit as st
import pandas as pd
import plotly.express as px
from ui_components import apply_custom_css
from engine import get_financial_metrics, apply_capital_rationing

st.set_page_config(page_title="Cognitive Capital Support", layout="wide")
apply_custom_css()

# --- STEP 0: SESSION STATE ---
if 'project_data' not in st.session_state:
    st.session_state.project_data = pd.DataFrame(columns=["Project", "Investment", "Year1", "Year2", "Year3", "Risk"])

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Decision Workflow")
nav = st.sidebar.radio("Navigate Process", [
    "1. Decision Context",
    "2. Financial Evaluation",
    "3. Forward-Looking Analysis",
    "4. Capital Trade-offs",
    "5. Uncertainty & Scenarios",
    "6. Decision Summary",
    "7. AI Interpretation Support"
])

# --- 1. DECISION CONTEXT ---
if nav == "1. Decision Context":
    st.markdown('<p class="section-header">Phase 1: Framing</p>', unsafe_allow_html=True)
    st.title("Strategic Decision Context")
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.text_area("Investment Objective", "e.g., Regional expansion vs efficiency upgrades")
            st.slider("Investment Horizon (Years)", 1, 10, 5)
        with col2:
            st.number_input("Total Capital Available (INR)", value=10000000, step=1000000, key="global_budget")
            st.select_slider("Risk Appetite", options=["Conservative", "Moderate", "Growth-Oriented"])

# --- 2. PROJECT FINANCIAL EVALUATION ---
elif nav == "2. Financial Evaluation":
    st.title("Project Financial Merit")
    st.markdown("Enter individual project estimates below to calculate core metrics.")
    
    with st.expander("Add Project Proposal", expanded=True):
        c1, c2, c3 = st.columns(3)
        name = c1.text_input("Project Name")
        inv = c2.number_input("Initial Capex (INR)", min_value=0)
        risk = c3.selectbox("Risk Profile", ["Low", "Medium", "High"])
        
        y1 = st.number_input("Year 1 Cash Flow", value=0)
        y2 = st.number_input("Year 2 Cash Flow", value=0)
        y3 = st.number_input("Year 3 Cash Flow", value=0)
        
        if st.button("Calculate & Save"):
            metrics = get_financial_metrics(inv, [y1, y2, y3], 0.10) # 10% Hurdle Rate
            new_row = pd.DataFrame([{"Project": name, "Investment": inv, "NPV": metrics['NPV'], "PI": metrics['PI'], "Risk": risk}])
            st.session_state.project_data = pd.concat([st.session_state.project_data, new_row], ignore_index=True)

    st.subheader("Current Proposal Queue")
    st.table(st.session_state.project_data)

# --- 4. CAPITAL TRADE-OFFS (Signature Section) ---
elif nav == "4. Capital Trade-offs":
    st.title("Capital Rationing & Prioritization")
    st.write("Solving the 'Capital Scarcity' problem: What must be given up?")
    
    budget = st.number_input("Apply Budget Constraint (INR)", value=10000000)
    
    if not st.session_state.project_data.empty:
        results, spent = apply_capital_rationing(st.session_state.project_data, budget)
        
        m1, m2 = st.columns(2)
        m1.metric("Budget Utilized", f"INR {spent:,}")
        m2.metric("Portfolio PI", round(results[results['Decision'] == '🟢 Fund']['PI'].mean(), 2))
        
        st.dataframe(results.style.applymap(lambda x: 'background-color: #dcfce7' if x == '🟢 Fund' else 'background-color: #fee2e2', subset=['Decision']), use_container_width=True)
        
        # Visualization of the Frontier
        fig = px.bar(results, x="Project", y="NPV", color="Decision", title="The Trade-off: Funded vs Deferred Projects")
        st.plotly_chart(fig)

# --- 7. AI INTERPRETATION SUPPORT ---
elif nav == "7. AI Interpretation Support":
    st.title("Analytical Interpretation")
    st.info("The AI provides reasoning behind the trade-offs shown in Phase 4.")
    user_q = st.chat_input("Ask about the decision logic...")
    if user_q:
        with st.chat_message("assistant"):
            st.write("Based on the Profitability Index (PI) logic, we prioritized projects that deliver the highest NPV per rupee of capital consumed. Deferred projects were not 'bad,' but were less capital-efficient under your current budget constraint.")

else:
    st.title(nav)
    st.write("Section under construction: Integrating forward-looking forecasting and scenario stress-tests.")
