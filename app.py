import streamlit as st
import sqlite3
from utils.lang import translations

st.set_page_config(page_title="DisasterGuard AI", page_icon="🌍", layout="wide")

# ---------------- LANGUAGE ----------------
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
t = translations.get(lang, translations["English"])

# ---------------- DB RESET FIX (IMPORTANT) ----------------
conn = sqlite3.connect("disasterguard.db", check_same_thread=False)
cursor = conn.cursor()

# 🔥 FIX: DROP OLD BROKEN TABLE
cursor.execute("DROP TABLE IF EXISTS reports")

# 🔥 CREATE NEW CORRECT TABLE
cursor.execute("""
CREATE TABLE reports (
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
conn.close()

# ---------------- UI ----------------
st.title("🌍 " + t.get("title", "Disaster Management System"))
st.markdown(f"### {t.get('welcome', 'Welcome')}")
st.success(t.get("system", "System Active"))

st.write("---")
st.subheader("📊 Dashboard")

# ---------------- DB READ ----------------
conn = sqlite3.connect("disasterguard.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM reports")
total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM reports WHERE status='Pending'")
pending = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM reports WHERE status='Rescued'")
rescued = cursor.fetchone()[0]

conn.close()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total", total)

with col2:
    st.metric("Pending", pending)

with col3:
    st.metric("Rescued", rescued)

st.write("---")
st.info("Dashboard Loaded 🚀")