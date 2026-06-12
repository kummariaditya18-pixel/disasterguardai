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
# UI (FIXED SAFELY - NO LAYOUT CHANGE)
# -----------------------------
st.title("🌍 " + t.get("title", "Disaster Management System"))

st.markdown(f"### {t.get('welcome', 'Welcome')}")

st.success(t.get("system", "System Active"))

st.write("---")

st.subheader("📊 Dashboard")

# -----------------------------
# SAFE DATABASE CONNECT
# -----------------------------
conn = sqlite3.connect("disasterguard.db", check_same_thread=False)
cursor = conn.cursor()

# -----------------------------
# SAFE TABLE HANDLING (NO CRASH)
# -----------------------------
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

# -----------------------------
# SAFE QUERIES (NO CRASH)
# -----------------------------
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
    st.metric(t.get("dashboard", {}).get("total", "Total"), total)

with col2:
    st.metric(t.get("dashboard", {}).get("pending", "Pending"), pending)

with col3:
    st.metric(t.get("dashboard", {}).get("rescued", "Rescued"), rescued)

st.write("---")

st.info(t.get("loaded", "DisasterGuard AI Dashboard Loaded Successfully 🚀"))