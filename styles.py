import streamlit as st

def apply_theme():
    st.markdown("""
        <style>
        /* Professional Slate & White Theme */
        .stApp { background-color: #F8FAFC; }
        
        /* Step Navigation Styling */
        .stRadio > label { font-weight: 700; color: #1E293B; }
        
        /* Main Container Cards */
        .main-card {
            background-color: white;
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
        }
        
        /* Phase Headers */
        .phase-header {
            color: #2563EB;
            font-size: 0.85rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
