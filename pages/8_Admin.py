import streamlit as st
import pandas as pd
from utils.lang import translations
from utils.db import init_db, fetch_reports

# -----------------------------
# INIT DB (SAFETY)
# -----------------------------
init_db()

# -----------------------------
# LANGUAGE SYNC
# -----------------------------
lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations.get(lang, translations["English"])

def tr(key, fallback):
    return t.get("menu", {}).get(key, fallback)

# -----------------------------
# TITLE (UNCHANGED)
# -----------------------------
st.title("⚙️ " + tr("admin", "Admin Panel"))

st.write("🔐 Admin Control Panel")
st.markdown("---")

# -----------------------------
# ACTION BUTTONS (UNCHANGED)
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("Clear Reports"):
        st.warning("Demo action only (connect later)")

with col2:
    if st.button("Reset System"):
        st.error("Demo action only (connect later)")

st.markdown("---")

# -----------------------------
# CONNECTED REPORT DATA
# -----------------------------
rows = fetch_reports()

columns = [
    "id",
    "tracking_id",
    "name",
    "location",
    "disaster_type",
    "severity",
    "description",
    "image_path",
    "status"
]

df = pd.DataFrame(rows, columns=columns)

# -----------------------------
# DISPLAY REPORTS
# -----------------------------
st.subheader("📋 All Disaster Reports")

if df.empty:
    st.warning("⚠️ No reports found")
else:
    st.success(f"Total Reports: {len(df)}")
    st.dataframe(df, use_container_width=True)

st.markdown("---")

st.info("Admin Panel Connected Successfully 🚀")