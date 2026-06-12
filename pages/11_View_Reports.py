import streamlit as st
import sqlite3
import pandas as pd

from utils.lang import translations

# ---------------- LANGUAGE ----------------
lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations[lang]

# ---------------- TITLE ----------------
st.title("📋 " + t["menu"]["reports"])

# ---------------- DB ----------------
conn = sqlite3.connect("disasterguard.db", check_same_thread=False)

try:
    query = "SELECT * FROM reports ORDER BY tracking_id DESC"
    df = pd.read_sql_query(query, conn)

    if df.empty:
        st.warning("⚠️ " + t["status"]["pending"])
    else:

        st.success(f"{t['dashboard']['total']}: {len(df)}")

        st.dataframe(df, use_container_width=True)

        # ---------------- FILTER ----------------
        st.markdown("### 🔍 " + t["menu"]["reports"])

        disaster_types = ["All"] + sorted(df["disaster_type"].dropna().unique().tolist())

        selected = st.selectbox(
            "Filter",
            disaster_types,
            index=0
        )

        if selected != "All":
            st.dataframe(df[df["disaster_type"] == selected], use_container_width=True)

except Exception as e:
    st.error("❌ Database Error: " + str(e))

# ---------------- DEBUG ----------------
with st.expander("🔍 Debug Table Structure", expanded=False):
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(reports)")
    columns = cursor.fetchall()

    if columns:
        st.table(
            pd.DataFrame(
                columns,
                columns=["cid", "name", "type", "notnull", "default", "pk"]
            )
        )
    else:
        st.warning("No table structure found")

conn.close()