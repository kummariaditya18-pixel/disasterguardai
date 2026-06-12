import streamlit as st
import sqlite3
from utils.lang import translations
from utils.db import init_db, count_reports

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="DisasterGuard AI",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# INIT DATABASE (GLOBAL FIX)
# -----------------------------
init_db()

# -----------------------------
# LANGUAGE SETUP
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
# UI (UNCHANGED)
# -----------------------------
st.title("🌍 " + t.get("title", "Disaster Management System"))

st.markdown(f"### {t.get('welcome', 'Welcome')}")

st.success(t.get("system", "System Active"))

st.write("---")

st.subheader("📊 Dashboard")

# -----------------------------
# SHARED DATABASE DATA
# -----------------------------
total, pending, rescued = count_reports()

# -----------------------------
# METRICS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(t.get("dashboard", {}).get("total", "Total"), total)

with col2:
    st.metric(t.get("dashboard", {}).get("pending", "Pending"), pending)

with col3:
    st.metric(t.get("dashboard", {}).get("rescued", "Rescued"), rescued)

st.write("---")

st.info(t.get("loaded", "Dashboard Loaded 🚀"))