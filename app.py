import streamlit as st
import sqlite3
from utils.lang import translations

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="DisasterGuard AI",
    page_icon="🌍",
    layout="wide"
)

# ---------------- LANGUAGE SELECTOR ----------------
if "lang" not in st.session_state:
    st.session_state.lang = "English"

lang_options = list(translations.keys())

selected_lang = st.sidebar.selectbox(
    "🌐 Language",
    lang_options,
    index=lang_options.index(st.session_state.lang)
)

if selected_lang != st.session_state.lang:
    st.session_state.lang = selected_lang
    st.rerun()

lang = st.session_state.lang
t = translations.get(lang, translations["English"])


# ---------------- SAFE DB ----------------
def get_counts():
    conn = sqlite3.connect("disasterguard.db", check_same_thread=False)
    cursor = conn.cursor()

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

    cursor.execute("SELECT COUNT(*) FROM reports")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE status='Pending'")
    pending = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE status='Rescued'")
    rescued = cursor.fetchone()[0]

    conn.close()

    return total, pending, rescued


# ---------------- UI ----------------
st.title("🌍 " + t.get("title", "DisasterGuard AI"))

st.markdown(f"### {t.get('welcome', 'Welcome')}")

st.success(t.get("system", "System Active"))

st.write("---")

# ---------------- DASHBOARD TITLE FIX ----------------
st.subheader("📊 " + t.get("dashboard_title", "Dashboard"))

# ---------------- DATA ----------------
total, pending, rescued = get_counts()

dashboard = t.get("dashboard", {})

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(dashboard.get("total", "Total"), total)

with col2:
    st.metric(dashboard.get("pending", "Pending"), pending)

with col3:
    st.metric(dashboard.get("rescued", "Rescued"), rescued)

st.write("---")

st.info(t.get("loaded", "DisasterGuard AI Dashboard Loaded Successfully 🚀"))