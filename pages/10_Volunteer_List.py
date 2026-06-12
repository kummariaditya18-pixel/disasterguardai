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
st.title("👥 " + tr("vol_list", "Volunteer List"))

# ---------------- VOLUNTEER SECTION (UNCHANGED LOGIC) ----------------
st.subheader("📋 Registered Volunteers")

# Example static data (replace with DB later if you have)
volunteers = [
    {"name": "Ravi", "location": "Vijayawada"},
    {"name": "Sita", "location": "Guntur"},
    {"name": "John", "location": "Hyderabad"}
]

for v in volunteers:
    st.write(f"👤 {v['name']} - 📍 {v['location']}")

st.markdown("---")

st.info("Volunteer List Loaded Successfully 🚀")