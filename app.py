import streamlit as st
import sqlite3
from utils.lang import translations

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="DisasterGuard AI",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# LANGUAGE SETUP
# -----------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "English"

lang_map = {
    "English": "English",
    "Hindi": "Hindi",
    "Telugu": "Telugu"
}

selected = st.sidebar.selectbox(
    "🌐 Choose Language",
    list(lang_map.keys()),
    index=list(lang_map.keys()).index(st.session_state.lang)
)

if selected != st.session_state.lang:
    st.session_state.lang = selected
    st.rerun()

lang = st.session_state.lang

if lang not in translations:
    lang = "English"

t = translations[lang]

# -----------------------------
# UI (UNCHANGED)
# -----------------------------
st.title("🌍 " + t["title"])

st.markdown(f"### {t['welcome']}")

st.success(t["system"])

st.write("---")

st.subheader("📊 Dashboard")

# -----------------------------
# FIX ONLY HERE (DATABASE CONNECT)
# -----------------------------
conn = sqlite3.connect("disasterguard.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM reports")
total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM reports WHERE status='Pending'")
pending = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM reports WHERE status='Rescued'")
rescued = cursor.fetchone()[0]

conn.close()

# -----------------------------
# UI METRICS (UNCHANGED STYLE)
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(t["dashboard"]["total"], total)

with col2:
    st.metric(t["dashboard"]["pending"], pending)

with col3:
    st.metric(t["dashboard"]["rescued"], rescued)

st.write("---")

st.info("DisasterGuard AI Dashboard Loaded Successfully 🚀")