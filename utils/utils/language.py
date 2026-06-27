import streamlit as st
from utils.lang import translations


def get_lang():
    if "lang" not in st.session_state:
        st.session_state.lang = "English"

    return st.session_state.lang


def get_t():
    lang = get_lang()

    if lang not in translations:
        lang = "English"

    return translations[lang]
