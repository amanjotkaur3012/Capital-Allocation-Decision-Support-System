import streamlit as st
import pandas as pd
import plotly.express as px
from calculations import calculate_metrics, solve_capital_rationing
from ui_components import apply_custom_style, header_component

st.set_page_config(page_title="Capital Allocation AI", layout="wide")
apply_custom_style()
header_component()

# --- Sidebar: Global Assumptions ---
with st.sidebar:
    st.header("Global Parameters")
    wacc = st.slider("Hurdle Rate (WACC) %", 5.0, 20.0, 10.0) / 100
    budget = st.number_input("Total Capital Budget ($M)", value=1000.0)
    
    st.divider()
    st.info("AI Assistant: Use the chat below to interpret your portfolio results.")

# --- Session State for Project Data ---
if 'projects' not in st.session_state:
    st.session_state.projects = pd.DataFrame(columns=[
        "Project Name", "Investment", "Year1", "Year2", "Year3", "Year4", "Year5"
    ])

# --- Input Section ---
with st.expander("➕ Add New Investment Proposal", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Project Name", placeholder="e.g., Solar Farm Phase II")
        inv = st.number_input("Initial Investment ($M)", min_value=0.0)
    with col2:
        st.write("Forecasted Annual Cash Flows ($M)")
        cfs = [st.number_input(f"Year {i}", value=0.0, key=f"y{i}") for i in range(1, 6)]
    
    if st.button("Submit Project for Evaluation"):
        new_row = {"Project Name": name, "Investment": inv, 
                   "Year1": cfs[0], "Year2": cfs[1], "Year3": cfs[2], "Year4": cfs[3], "Year5": cfs[4]}
        st.session_state.projects = pd.concat([st.session_state.projects, pd.DataFrame([new_row])], ignore_index=True)

# --- Analysis Section ---
if not st.session_state.projects.empty:
    df = st.session_state.projects.copy()
    
    # Calculate Metrics for each row
    results = []
    for idx, row in df.iterrows():
        m = calculate_metrics(row['Investment'], [row['Year1'], row['Year2'], row['Year3'], row['Year4'], row['Year5']], wacc)
        results.append(m)
    
    res_df = pd.concat([df, pd.DataFrame(results)], axis=1)
    
    # Portfolio Level View
    st.header("📊 Portfolio Evaluation")
    
    # Metrics Overview
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Proposed Capex", f"${df['Investment'].sum():,.1f}M")
    c2.metric("Portfolio Avg IRR", f"{res_df['IRR'].mean()*100:.2f}%")
    c3.metric("Budget Utilization", f"{(df['Investment'].sum()/budget)*100:.1f}%")

    # Capital Rationing Logic
    selected_names, spent = solve_capital_rationing(res_df, budget)
    res_df['Allocation Status'] = res_df['Project Name'].apply(lambda x: "✅ Funded" if x in selected_names else "❌ Deferred")

    # Visualization: NPV vs IRR
    fig = px.scatter(res_df, x="IRR", y="NPV", size="Investment", color="Allocation Status",
                     hover_name="Project Name", title="Project Risk-Return Matrix (Bubble Size = Investment)")
    st.plotly_chart(fig, use_container_width=True)

    # Detailed Table
    st.subheader("Project Ranking & Selection")
    st.dataframe(res_df.style.background_gradient(subset=['NPV', 'IRR'], cmap='Blues'), use_container_width=True)

    # Conversational "AI" (Heuristic based for logic stability)
    st.divider()
    st.subheader("🤖 Financial Reasoning Assistant")
    user_q = st.chat_input("Ask about the portfolio (e.g., 'Which project is most sensitive to interest rates?')")
    if user_q:
        with st.chat_message("assistant"):
            if "budget" in user_q.lower():
                st.write(f"Given your ${budget}M limit, we had to defer {len(res_df)-len(selected_names)} projects. The primary reason for deferral was lower Profitability Index (PI) compared to the funded set.")
            else:
                st.write("Based on the current WACC of {:.1%}, Project {} offers the best wealth creation per dollar invested.".format(wacc, res_df.iloc[res_df['PI'].idxmax()]['Project Name']))

else:
    st.warning("No projects submitted. Please input project data in the expander above.")
