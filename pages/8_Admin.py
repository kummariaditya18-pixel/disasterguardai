import streamlit as st
import pandas as pd
import sqlite3

from utils.lang import translations
from utils.db import init_db, fetch_reports, get_conn
from utils.auth import login, logout, is_admin

# ---------------- INIT DB ----------------
init_db()

# ---------------- LANGUAGE SAFE FIX ----------------
lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations.get(lang, translations["English"])
menu = t.get("menu", {})

def tr(key, fallback):
    return menu.get(key, fallback)

# ---------------- LOGIN SYSTEM ----------------
if not is_admin():
    st.title("🔐 " + tr("admin", "Admin Panel"))

    st.write("Login to access admin panel")

    username = st.text_input(tr("username", "Username"))
    password = st.text_input(tr("password", "Password"), type="password")

    if st.button(tr("login", "Login")):
        if login(username, password):
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()

# ---------------- ADMIN DASHBOARD ----------------
st.title("⚙️ " + tr("admin", "Admin Panel"))

st.success(f"{tr('welcome', 'Welcome')} {st.session_state.get('admin_user')}")

if st.button(tr("logout", "Logout")):
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

# ---------------- SHOW REPORTS ----------------
st.subheader(tr("reports", "Disaster Reports"))

if df.empty:
    st.warning(tr("no_data", "No reports found"))
else:
    st.success(f"{tr('total', 'Total')}: {len(df)}")
    st.dataframe(df, use_container_width=True)

st.write("---")

# ---------------- STATUS UPDATE ----------------
st.subheader(tr("update", "Update Report Status"))

conn = get_conn()
cursor = conn.cursor()

report_id = st.text_input(tr("report_id", "Report ID"))

status_options = [
    tr("pending", "Pending"),
    tr("rescued", "Rescued")
]

new_status = st.selectbox(tr("status", "Status"), status_options)

if st.button(tr("update_btn", "Update")):
    if report_id:
        cursor.execute(
            "UPDATE reports SET status=? WHERE id=?",
            (new_status, report_id)
        )
        conn.commit()
        st.success(tr("updated", "Status updated successfully"))
        st.rerun()

conn.close()