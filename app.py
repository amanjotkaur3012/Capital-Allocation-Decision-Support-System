import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from ui_components import apply_enterprise_style, draw_sidebar_nav
from calculations import calculate_metrics, solve_capital_rationing

st.set_page_config(page_title="CapitalIQ-AI Enterprise", layout="wide")
apply_enterprise_style()

# Sidebar & Navigation
page, total_budget = draw_sidebar_nav()

if page == "📊 Executive Summary":
    st.header("Executive Dashboard")
    
    # Top Row Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Projects Funded", "12", "Total: 50", delta_color="normal")
    m2.metric("Capital Deployed", "₹14.94M", "Util: 99.6%", delta_color="normal")
    m3.metric("Projected NPV", "₹2.34M", "Payback: 0.8 Yrs", delta_color="normal")
    m4.metric("Avg Risk Score", "7.08", "Max: 6.5", delta_color="inverse")

    st.markdown("---")
    
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("Capital Allocation by Department")
        # Mock Data for the Stacked Bar Chart
        dept_data = pd.DataFrame({
            'Department': ['Supply Chain', 'Infrastructure', 'Marketing', 'R&D', 'HR', 'IT Transformation'],
            'Base': [3.0, 1.2, 1.5, 0.16, 0.74, 0.8],
            'Growth': [2.6, 1.4, 0.54, 0.0, 0.95, 0.0],
            'Strategic': [1.7, 0.0, 0.0, 0.0, 0.45, 0.0],
            'ROI': [25, 22, 18, 12, 20, 15]
        })
        
        fig = px.bar(dept_data, x='Department', y=['Base', 'Growth', 'Strategic'],
                     title="Budget Distribution (Colored by Project Type)",
                     color_discrete_sequence=['#96D701', '#E8F11B', '#00D1FF'])
        
        fig.update_layout(template="plotly_dark", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("Actionable Reports")
        st.button("📄 Download Official PDF Report")
        
        st.markdown("#### 📈 Top ROI Drivers")
        importance_df = pd.DataFrame({
            'Feature': ['Market_Trend_Index', 'Risk_Score', 'Investment_Capital', 'Duration_Months', 'Strategic_Alignment'],
            'Importance': [0.477, 0.192, 0.165, 0.109, 0.054]
        })
        st.table(importance_df)

elif page == "📉 Scenario Manager":
    st.header("What-If Scenario Analysis")
    st.info("Simulate changes in market volatility and interest rates to see portfolio impact.")
    # Add sensitivity sliders here
    
elif page == "🏠 Home & Data":
    st.header("Project Intake & Database")
    uploaded_file = st.file_uploader("Upload Project Proposals (CSV/XLSX)")
    if uploaded_file:
        st.success("Data ingested successfully. Ready for AI Evaluation.")

# Placeholder for other pages to keep the student's project structure
else:
    st.title(f"{page}")
    st.write("This module is currently processing live data...")
