import streamlit as st
from utils.lang import translations

# ---------------- LANGUAGE ----------------
lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations[lang]

# ---------------- SAFE TRANSLATION HELPER ----------------
def tr(key, fallback):
    return t.get("menu", {}).get(key, fallback)

# ---------------- TITLE (FIXED ONLY) ----------------
st.title("⚙️ " + tr("admin", "Admin Panel"))

# ---------------- SIMPLE ADMIN UI (UNCHANGED IDEA) ----------------
st.write("🔐 Admin Control Panel")

st.markdown("---")

st.subheader("📊 System Controls")

st.write("Manage reports, users, and system settings here.")

# ---------------- SAMPLE ACTIONS (PLACEHOLDER) ----------------
col1, col2 = st.columns(2)

with col1:
    if st.button("Clear Reports"):
        st.warning("Reports cleared (demo action)")

with col2:
    if st.button("Reset System"):
        st.error("System reset (demo action)")

st.markdown("---")

st.info("Admin Panel Loaded Successfully 🚀")