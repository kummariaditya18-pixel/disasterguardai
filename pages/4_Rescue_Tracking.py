import streamlit as st
import sqlite3
from utils.lang import translations

# ---------------- LANGUAGE ----------------
lang = st.session_state.get("lang", "English")
t = translations.get(lang, translations["English"])

menu = t.get("menu", {})
form = t.get("form", {})


def tr_menu(key, fallback):
    return menu.get(key, fallback)


def tr_form(key, fallback):
    return form.get(key, fallback)


# ---------------- TITLE (UNCHANGED LAYOUT) ----------------
st.title("🚑 " + tr_menu("tracking", "Rescue Tracking"))

# ---------------- INPUT ----------------
track_id = st.text_input("Enter Tracking ID")

# ---------------- SEARCH ----------------
if st.button("Search"):
    conn = sqlite3.connect("disasterguard.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reports WHERE tracking_id = ?", (track_id,))

    result = cursor.fetchone()
    conn.close()

    if result:
        st.success(t.get("system", "System Active"))

        st.write("🆔", result[0])
        st.write("👤", result[1])
        st.write("📍", result[2])
        st.write("🌪️", result[3])
        st.write("⚠️", result[4])
        st.write("📝", result[5])
        st.write("⏰", result[7])

        # ---------------- STATUS ----------------
        status = result[8] if len(result) > 8 else "Pending"

        st.markdown("### 🚦 " + tr_menu("status", "Current Status"))

        if status == "Pending":
            st.warning("🟡 " + tr_form("low", "Pending"))

        elif status == "In Progress":
            st.info("🔵 " + tr_form("medium", "In Progress"))

        elif status == "Solved":
            st.success("🟢 " + tr_form("high", "Solved"))

        else:
            st.error("Unknown")

    else:
        st.error(tr_menu("not_found", "Not found"))
