import streamlit as st
from utils.lang import translations

lang = st.session_state.get("lang", "English")
t = translations.get(lang, translations["English"])

st.title("🚨 " + t["menu"]["report"])

st.write(t["welcome"])

with st.form("report_form"):
    name = st.text_input("Name")
    location = st.text_input("Location")
    description = st.text_area("Description")

    submit = st.form_submit_button(t["menu"]["report"])

    if submit:
        st.success("Report Submitted Successfully")