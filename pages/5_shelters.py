import streamlit as st
from utils.lang import translations

# ---------------- LANGUAGE ----------------
lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations[lang]

# ---------------- PAGE TITLE ----------------
st.title("🏕️ " + t["menu"]["shelters"])

# ---------------- SHELTER LIST ----------------
st.write("🏫 Government School Shelter")
st.write("🏛️ Community Hall Shelter")
st.write("🚑 District Relief Camp")