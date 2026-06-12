import streamlit as st

def get_lang():
    return st.session_state.get("lang", "English")