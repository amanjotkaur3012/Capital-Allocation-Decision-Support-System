import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
        .stApp { background-color: #FDFDFD; }
        .decision-card {
            background-color: #FFFFFF;
            padding: 25px;
            border-radius: 10px;
            border-left: 5px solid #1E3A8A;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }
        .section-header {
            color: #1E3A8A;
            font-size: 0.8rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1.5px;
        }
        </style>
    """, unsafe_allow_html=True)
