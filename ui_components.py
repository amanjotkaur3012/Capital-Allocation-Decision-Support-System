import streamlit as st

def apply_enterprise_style():
    st.markdown("""
        <style>
        /* Main background */
        .stApp { background-color: #0E1117; }
        
        /* Metric Card Styling */
        div[data-testid="stMetric"] {
            background-color: #1A1C24;
            border: 1px solid #2D2F39;
            padding: 20px;
            border-radius: 10px;
            color: white;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #11141B;
            border-right: 1px solid #2D2F39;
        }

        /* Custom Header Colors */
        h1, h2, h3 { color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
        
        /* Buttons */
        .stButton>button {
            background-color: #1A1C24;
            color: #00D1FF;
            border: 1px solid #00D1FF;
            border-radius: 5px;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

def draw_sidebar_nav():
    st.sidebar.title("CAPITALIQ-AI")
    st.sidebar.caption("ENTERPRISE EDITION")
    st.sidebar.markdown("---")
    
    menu = st.sidebar.radio("Navigation", [
        "🏠 Home & Data",
        "📊 Executive Summary",
        "💡 AI Insights",
        "📈 Efficient Frontier",
        "⚙️ Optimization Report",
        "🗺️ Strategic 3D Map",
        "📉 Scenario Manager",
        "📝 AI Deal Memos"
    ])
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("Constraints & Sandbox")
    with st.sidebar.expander("WACC Builder (CAPM)"):
        st.number_input("Risk Free Rate (%)", 2.0, 10.0, 7.0)
        st.number_input("Beta", 0.5, 2.0, 1.1)
    
    budget = st.sidebar.number_input("Total Budget (INR)", value=150000000.0)
    return menu, budget
