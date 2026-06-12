import streamlit as st
import sqlite3
import pandas as pd

from utils.lang import translations

# ---------------- LANGUAGE ----------------
lang = st.session_state.get("lang", "English")
t = translations.get(lang, translations["English"])

st.title("⚙️ " + t["menu"]["admin"])

# ---------------- DB CONNECT ----------------
conn = sqlite3.connect("disasterguard.db", check_same_thread=False)

# ---------------- LOAD DATA ----------------
query = "SELECT * FROM reports"
df = pd.read_sql_query(query, conn)

conn.close()

# ---------------- EMPTY CHECK ----------------
if df.empty:
    st.warning("No reports found")
    st.stop()

# ---------------- CLEAN TABLE ----------------
df.columns = [
    "Tracking ID",
    "Name",
    "Location",
    "Disaster Type",
    "Severity",
    "Description",
    "Image Path",
    "Created At"
]

# ---------------- DISPLAY TABLE ----------------
st.subheader("📊 Disaster Reports Table")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# ---------------- OPTIONAL FILTERS ----------------
st.markdown("---")
st.subheader("🔍 Filter Reports")

status_filter = st.selectbox(
    "Filter by Severity",
    ["All", "Low 🟢", "Medium 🟡", "High 🔴", "Critical 🚨"]
)

if status_filter != "All":
    filtered_df = df[df["Severity"] == status_filter]
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)