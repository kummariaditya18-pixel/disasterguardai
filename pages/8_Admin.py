import streamlit as st
from utils.lang import translations

# ---------------- LANGUAGE SYNC (IMPORTANT FIX) ----------------
if "lang" not in st.session_state:
    st.session_state.lang = "English"

lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations.get(lang, translations["English"])

# ---------------- SAFE TRANSLATION HELPER ----------------
def tr(key, fallback):
    return t.get("menu", {}).get(key, fallback)

# ---------------- TITLE (UNCHANGED LAYOUT) ----------------
st.title("⚙️ " + tr("admin", "Admin Panel"))

# ---------------- ADMIN UI (UNCHANGED DESIGN) ----------------
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

st.info(t.get("system", "Admin Panel Loaded Successfully 🚀"))