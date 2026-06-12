import streamlit as st
import pandas as pd
import sqlite3

from utils.db import init_db, fetch_reports, get_conn
from utils.auth import login, logout, is_admin

init_db()

# ---------------- LOGIN PAGE (BLOCK ACCESS) ----------------
if not is_admin():
    st.title("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login(username, password):
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()  # 🔥 BLOCK EVERYTHING BELOW

# ---------------- ADMIN DASHBOARD ----------------
st.title("⚙️ Admin Panel")

st.success(f"Welcome Admin: {st.session_state.get('admin_user')}")

if st.button("Logout"):
    logout()
    st.rerun()

st.write("---")

# ---------------- LOAD DATA ----------------
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

st.subheader("📋 All Disaster Reports")

if df.empty:
    st.warning("No reports found")
else:
    st.dataframe(df, use_container_width=True)

# ---------------- STATUS UPDATE (ADMIN ONLY) ----------------
st.write("---")
st.subheader("🔄 Update Report Status")

conn = get_conn()
cursor = conn.cursor()

report_id = st.text_input("Enter Report ID")
new_status = st.selectbox("Change Status", ["Pending", "Rescued"])

if st.button("Update Status"):
    if report_id:
        cursor.execute(
            "UPDATE reports SET status=? WHERE id=?",
            (new_status, report_id)
        )
        conn.commit()
        st.success("Status updated successfully")
        st.rerun()

conn.close()