import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        .main { background-color: #f5f7f9; }
        .stMetric { 
            background-color: #ffffff; 
            padding: 15px; 
            border-radius: 10px; 
            box-shadow: 0 2px 4px rgba(0,0,0,0.05); 
        }
        .reportview-container .main .block-container { padding-top: 2rem; }
        h1 { color: #002D62; font-weight: 800; }
        h2 { color: #0047AB; }
        </style>
    """, unsafe_allow_html=True)

def header_component():
    st.title("🏛️ Strategic Capital Allocation System")
    st.markdown("""
    **Executive Decision Support** | Transparency • Rigor • Capital Discipline
    ---
    """)
