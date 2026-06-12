import streamlit as st
import pandas as pd
import os

from utils.lang import translations

# ---------------- LANGUAGE ----------------
lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations[lang]

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title=t["menu"]["admin"],
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("⚙️ " + t["menu"]["admin"])

# ---------------- FILE PATH ----------------
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

CSV_FILE = os.path.join(
    PROJECT_ROOT,
    "data",
    "reports.csv"
)

# ---------------- LOAD DATA ----------------
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame()

if df.empty:
    st.warning(t["status"]["pending"])
    st.stop()

df = df.fillna("")

# ---------------- STATS ----------------
total_reports = len(df)

pending_reports = len(
    df[df["status"] == "Pending"]
)

rescued_reports = len(
    df[df["status"] == "Rescued"]
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        t["dashboard"]["total"],
        total_reports
    )

with col2:
    st.metric(
        t["dashboard"]["pending"],
        pending_reports
    )

with col3:
    st.metric(
        t["dashboard"]["rescued"],
        rescued_reports
    )

st.markdown("---")

# ---------------- REPORTS ----------------
st.subheader("🚨 " + t["menu"]["reports"])

st.dataframe(
    df[
        [
            "tracking_id",
            "name",
            "location",
            "disaster_type",
            "severity",
            "status"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

st.markdown("---")

# ---------------- ADMIN PANEL ----------------
st.subheader("🛠️ " + t["menu"]["admin"])

track_id = st.text_input(
    t["menu"]["tracking"]
)

new_status = st.selectbox(
    "Status",
    [
        "Pending",
        "In Progress",
        "Rescued"
    ]
)

if st.button(t["menu"]["admin"]):

    if not track_id.strip():
        st.error("Tracking ID required")

    else:

        mask = (
            df["tracking_id"]
            .astype(str)
            == track_id.strip()
        )

        if mask.any():

            df.loc[
                mask,
                "status"
            ] = new_status

            df.to_csv(
                CSV_FILE,
                index=False
            )

            st.success(
                "Status updated successfully"
            )

            st.rerun()

        else:
            st.error(
                "Tracking ID not found"
            )