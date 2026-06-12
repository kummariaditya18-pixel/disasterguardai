import streamlit as st
import sqlite3
import pandas as pd
from utils.lang import translations

# ---------------- LANGUAGE SYNC ----------------
if "lang" not in st.session_state:
    st.session_state.lang = "English"

lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations.get(lang, translations["English"])

def tr(key, fallback):
    return t.get("menu", {}).get(key, fallback)

# ---------------- TITLE ----------------
st.title("⚙️ " + tr("admin", "Admin Panel"))

# ---------------- ADMIN UI ----------------
st.write("🔐 Admin Control Panel")

st.markdown("---")

st.subheader("📊 System Controls")

st.write("Manage reports, users, and system settings here.")

# ---------------- ACTION BUTTONS ----------------
col1, col2 = st.columns(2)

with col1:
    if st.button("Clear Reports"):
        st.warning("Reports cleared (demo action)")

with col2:
    if st.button("Reset System"):
        st.error("System reset (demo action)")

st.markdown("---")

# ---------------- DATABASE CONNECTION ----------------
conn = sqlite3.connect("disasterguard.db", check_same_thread=False)
cursor = conn.cursor()

# Ensure table exists (safe)
cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tracking_id TEXT,
    name TEXT,
    location TEXT,
    disaster_type TEXT,
    severity TEXT,
    description TEXT,
    image_path TEXT,
    status TEXT DEFAULT 'Pending'
)
""")

conn.commit()

# ---------------- LOAD REPORTS ----------------
df = pd.read_sql_query("SELECT * FROM reports ORDER BY id DESC", conn)

conn.close()

# ---------------- DISPLAY REPORTS ----------------
st.subheader("📋 All Disaster Reports")

if df.empty:
    st.warning("⚠️ No reports found.")
else:
    st.success(f"Total Reports: {len(df)}")
    st.dataframe(df, use_container_width=True)

st.markdown("---")

st.info(t.get("system", "Admin Panel Loaded Successfully 🚀"))