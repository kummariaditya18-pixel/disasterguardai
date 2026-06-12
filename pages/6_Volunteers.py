import streamlit as st
from backend.database import save_volunteer
from utils.lang import translations

# ---------------- LANGUAGE ----------------
lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations[lang]

# ---------------- TITLE ----------------
st.title("👥 " + t["menu"]["volunteers"])

# ---------------- FORM ----------------
name = st.text_input("Name")
phone = st.text_input("Phone")

skill = st.selectbox(
    "Skill",
    [
        "Medical",
        "Rescue",
        "Food Distribution",
        "Transport"
    ]
)

# ---------------- BUTTON ----------------
if st.button(t["menu"]["volunteers"]):

    save_volunteer(
        name,
        phone,
        skill
    )

    st.success(t["system"])