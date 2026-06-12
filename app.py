import streamlit as st
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
# UI
# -----------------------------
st.title("🌍 " + t["title"])

st.markdown(f"### {t['welcome']}")

st.success(t["system"])

st.write("---")

st.subheader("📊 Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(t["dashboard"]["total"], "0")

with col2:
    st.metric(t["dashboard"]["pending"], "0")

with col3:
    st.metric(t["dashboard"]["rescued"], "0")

st.write("---")

st.info("DisasterGuard AI Dashboard Loaded Successfully 🚀")