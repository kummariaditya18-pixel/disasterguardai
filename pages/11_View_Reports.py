import streamlit as st
import sqlite3
import pandas as pd
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
st.title("📋 " + tr("reports", "View Reports"))

# ---------------- DATABASE ----------------
conn = sqlite3.connect("disasterguard.db", check_same_thread=False)
cursor = conn.cursor()

# ---------------- LOAD DATA ----------------
try:
    query = "SELECT * FROM reports ORDER BY tracking_id DESC"
    df = pd.read_sql_query(query, conn)

    if df.empty:
        st.warning("⚠️ No disaster reports found.")
    else:
        st.success(f"✅ Total Reports: {len(df)}")
        st.dataframe(df, use_container_width=True)

        # ---------------- FILTER ----------------
        st.markdown("### 🔍 Filter Reports")

        disaster_types = ["All"] + sorted(df["disaster_type"].dropna().unique().tolist())
        selected = st.selectbox("Filter by Disaster Type", disaster_types)

        if selected != "All":
            st.dataframe(df[df["disaster_type"] == selected], use_container_width=True)

except Exception as e:
    st.error(f"❌ Database Error: {e}")

# ---------------- DEBUG TABLE ----------------
with st.expander("🔍 Debug Table Structure", expanded=False):
    cursor.execute("PRAGMA table_info(reports)")
    columns = cursor.fetchall()

    if columns:
        st.table(pd.DataFrame(columns, columns=["cid", "name", "type", "notnull", "default", "pk"]))
    else:
        st.warning("No table structure found.")

# ---------------- CLOSE CONNECTION ----------------
conn.close()
