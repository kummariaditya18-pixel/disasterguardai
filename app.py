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
# LANGUAGE SETUP (SAFE FIX)
# -----------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "English"

lang_map = ["English", "Hindi", "Telugu"]

selected = st.sidebar.selectbox(
    "🌐 Choose Language",
    lang_map,
    index=lang_map.index(st.session_state.lang)
)

if selected != st.session_state.lang:
    st.session_state.lang = selected
    st.rerun()

lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations.get(lang, translations["English"])

# -----------------------------
# SAFE KEYS (NO CRASH IF MISSING)
# -----------------------------
title = t.get("title", "Disaster Management System")
welcome = t.get("welcome", "Welcome")
system = t.get("system", "System Active")
dashboard = t.get("dashboard", {})

# -----------------------------
# UI (UNCHANGED LAYOUT)
# -----------------------------
st.title("🌍 " + title)

st.markdown(f"### {welcome}")

st.success(system)

st.write("---")

st.subheader("📊 Dashboard")

# -----------------------------
# DATABASE SAFE CONNECTION
# -----------------------------
conn = sqlite3.connect("disasterguard.db", check_same_thread=False)
cursor = conn.cursor()

# -----------------------------
# ENSURE TABLE EXISTS
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
# SAFE COUNT QUERIES
# -----------------------------
try:
    cursor.execute("SELECT COUNT(*) FROM reports")
    total = cursor.fetchone()[0]
except:
    total = 0

try:
    cursor.execute("SELECT COUNT(*) FROM reports WHERE status='Pending'")
    pending = cursor.fetchone()[0]
except:
    pending = 0

try:
    cursor.execute("SELECT COUNT(*) FROM reports WHERE status='Rescued'")
    rescued = cursor.fetchone()[0]
except:
    rescued = 0

conn.close()

# -----------------------------
# METRICS (UNCHANGED LAYOUT)
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(dashboard.get("total", "Total"), total)

with col2:
    st.metric(dashboard.get("pending", "Pending"), pending)

with col3:
    st.metric(dashboard.get("rescued", "Rescued"), rescued)

st.write("---")

st.info(system + " 🚀")