import streamlit as st
import pandas as pd
import os

from utils.lang import translations

lang = st.session_state.get("lang", "English")
t = translations.get(lang, translations["English"])

st.set_page_config(
    page_title=t["menu"]["tracking"],
    page_icon="🚑"
)

st.title("🚑 " + t["menu"]["tracking"])

DATA_FILE = "data/rescue_requests.csv"

track_id = st.text_input(t["menu"]["tracking"])

if st.button(t["menu"]["tracking"]):

    if not os.path.exists(DATA_FILE):
        st.error(t["status"]["pending"])
        st.stop()

    df = pd.read_csv(DATA_FILE)

    result = df[df["tracking_id"].astype(str) == track_id.strip()]

    if result.empty:
        st.error(t["status"]["pending"])
    else:
        r = result.iloc[0]

        st.success(t["system"])

        st.write("### " + t["menu"]["reports"])

        st.write("Name:", r["name"])
        st.write("Location:", r["location"])
        st.write("Disaster Type:", r["disaster_type"])
        st.write("Severity:", r["severity"])

        status = str(r["status"])

        if status == "Pending":
            st.progress(30)
            st.warning(t["status"]["pending"])

        elif status == "In Progress":
            st.progress(70)
            st.info("Rescue Team On The Way")

        elif status == "Rescued":
            st.progress(100)
            st.success(t["status"]["rescued"])