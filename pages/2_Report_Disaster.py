import streamlit as st
from utils.lang import translations
from utils.db import init_db, add_report
import uuid

# ---------------- INIT DB ----------------
init_db()

# ---------------- LANGUAGE ----------------
lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations.get(lang, translations["English"])
form = t.get("form", {})

# ---------------- TITLE ----------------
st.title("🚨 " + form.get("report_title", "Report Disaster"))

st.write(t.get("welcome", "Welcome"))

# ---------------- FORM ----------------
with st.form("report_form"):
    name = st.text_input(form.get("name", "Name"))
    location = st.text_input(form.get("location", "Location"))

    disaster_type = st.selectbox(
        form.get("disaster_type", "Disaster Type"),
        [
            form.get("flood", "Flood 🌊"),
            form.get("earthquake", "Earthquake 🌍"),
            form.get("storm", "Storm 🌪️"),
            form.get("fire", "Fire 🔥"),
        ],
    )

    severity = st.selectbox(
        form.get("severity", "Severity"),
        [
            form.get("low", "Low 🟢"),
            form.get("medium", "Medium 🟡"),
            form.get("high", "High 🔴"),
        ],
    )

    description = st.text_area(form.get("description", "Description"))

    image = st.file_uploader(
        form.get("upload", "Upload Image (Optional)"), type=["png", "jpg", "jpeg"]
    )

    submit = st.form_submit_button(form.get("submit", "Submit Report"))

    # ---------------- SAVE DATA ----------------
    if submit:
        tracking_id = str(uuid.uuid4())[:8]

        image_path = ""
        if image is not None:
            image_path = image.name

        add_report(
            tracking_id,
            name,
            location,
            disaster_type,
            severity,
            description,
            image_path,
        )

        st.success(form.get("success", "Report Submitted Successfully"))
        st.info("📌 Tracking ID: " + tracking_id)

# ---------------- INFO ----------------
st.write("---")
st.info(t.get("system", "System Active"))
