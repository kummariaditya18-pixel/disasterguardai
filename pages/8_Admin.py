import streamlit as st
import sqlite3
import pandas as pd
from utils.lang import translations

# ---------------- LANGUAGE ----------------
lang = st.session_state.get("lang", "English")
t = translations.get(lang, translations["English"])

def tr(key, fallback):
    return t.get("menu", {}).get(key, fallback)

# ---------------- TITLE ----------------
st.title("⚙️ " + tr("admin", "Admin Panel"))

st.write("🔐 Admin Control Panel")
st.markdown("---")

# ---------------- DB SAFE LOAD ----------------
conn = sqlite3.connect("disasterguard.db", check_same_thread=False)
cursor = conn.cursor()

try:
    cursor.execute("SELECT * FROM reports ORDER BY id DESC")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(rows, columns=columns)

except Exception as e:
    st.error(f"Database error: {e}")
    df = pd.DataFrame()

conn.close()

# ---------------- SHOW DATA ----------------
st.subheader("📋 All Reports")

if df.empty:
    st.warning("No reports found")
else:
    st.success(f"Total Reports: {len(df)}")
    st.dataframe(df, use_container_width=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button("Clear Reports"):
        st.warning("Demo action only")

with col2:
    if st.button("Reset System"):
        st.error("Demo action only")

st.info("Admin Loaded 🚀")