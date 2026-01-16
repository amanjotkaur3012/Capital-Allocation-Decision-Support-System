import streamlit as st
import pandas as pd
import plotly.express as px
from styles import apply_theme  # This matches the file we created in Step 1
from engine import calculate_capital_rationing

st.set_page_config(page_title="Strategic Capital Orchestrator", layout="wide")
apply_theme()

# --- Workflow Sidebar ---
st.sidebar.title("Decision Workflow")
step = st.sidebar.radio("Navigate Process", [
    "1️⃣ Decision Context",
    "2️⃣ Financial Evaluation",
    "3️⃣ Forward-Looking Analysis",
    "4️⃣ Capital Trade-offs",
    "5️⃣ Uncertainty & Scenarios",
    "6️⃣ Decision Summary",
    "7️⃣ AI Interpretation Support"
])

# Initialize session data
if 'projects' not in st.session_state:
    st.session_state.projects = pd.DataFrame([
        {"Project": "Factory Automation", "Investment": 4000000, "NPV": 1200000},
        {"Project": "Market Entry: Asia", "Investment": 6000000, "NPV": 2500000},
        {"Project": "Green Energy Pilot", "Investment": 3000000, "NPV": 500000}
    ])

# --- Step 1: Decision Context ---
if step == "1️⃣ Decision Context":
    st.markdown('<p class="phase-header">Phase 1: Framing</p>', unsafe_allow_html=True)
    st.title("Strategic Decision Context")
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Objective")
            st.text_area("Investment Mission", "Prioritize long-term growth while maintaining liquidity.")
            st.slider("Horizon (Years)", 1, 10, 5)
        with col2:
            st.subheader("Constraints")
            budget = st.number_input("Total Available Capital (INR)", value=10000000)
            st.select_slider("Risk Appetite", ["Conservative", "Moderate", "Aggressive"])

# --- Step 4: Capital Trade-offs (Your Signature Section) ---
elif step == "4️⃣ Capital Trade-offs":
    st.markdown('<p class="phase-header">Phase 4: Optimization</p>', unsafe_allow_html=True)
    st.title("Capital Rationing & Prioritization")
    
    budget_limit = st.slider("Adjust Capital Ceiling", 1000000, 15000000, 8000000)
    
    results, spent = calculate_capital_rationing(st.session_state.projects, budget_limit)
    
    m1, m2 = st.columns(2)
    m1.metric("Budget Utilization", f"INR {spent:,}", f"{(spent/budget_limit)*100:.1f}% used")
    m2.metric("Portfolio PI (Efficiency)", round(results[results['Decision'] == '🟢 Fund']['PI'].mean(), 2))

    st.subheader("Funding Recommendations")
    st.dataframe(results.style.applymap(lambda x: 'color: green' if x == '🟢 Fund' else 'color: red', subset=['Decision']), use_container_width=True)

    # Visualization of what we are losing (Opportunity Cost)
    fig = px.bar(results, x="Project", y="NPV", color="Decision", 
                 title="The Cost of Scarcity: Funded vs. Deferred NPV")
    st.plotly_chart(fig, use_container_width=True)

# Placeholder for Step 7
elif step == "7️⃣ AI Interpretation Support":
    st.title("Analytical Reasoning Assistant")
    st.info("Explainable AI: Understanding why the system prioritized specific projects.")
    st.chat_input("Ask about the trade-off logic...")

else:
    st.info(f"Section {step} is currently loading logic modules...")
