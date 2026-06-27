import streamlit as st
from backend.database import save_volunteer
from utils.lang import translations

lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations[lang]

st.title("👥 " + t["menu"]["volunteers"])

name = st.text_input(t.get("name", "Name"))

phone = st.text_input(t.get("phone", "Phone"))

skill = st.selectbox(
    t.get("skill", "Skill"), ["Medical", "Rescue", "Food Distribution", "Transport"]
)

if st.button(t["menu"]["volunteers"]):
    if name and phone:
        save_volunteer(name, phone, skill)

        st.success(t.get("system", "Volunteer Registered Successfully"))

    else:
        st.warning(t.get("fill_fields", "Please fill all fields"))
