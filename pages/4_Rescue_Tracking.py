import streamlit as st
import sqlite3

from utils.lang import translations

lang = st.session_state.get("lang", "English")
t = translations.get(lang, translations["English"])

st.title("🚑 " + t["menu"]["tracking"])

track_id = st.text_input("Enter Tracking ID")

# ---------------- SEARCH ----------------
if st.button("Search"):

    conn = sqlite3.connect("disasterguard.db", check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM reports WHERE tracking_id = ?",
        (track_id,)
    )

    result = cursor.fetchone()

    conn.close()

    if result:

        st.success(t["system"])

        st.write("🆔", result[0])
        st.write("👤", result[1])
        st.write("📍", result[2])
        st.write("🌪️", result[3])
        st.write("⚠️", result[4])
        st.write("📝", result[5])
        st.write("⏰", result[7])

        # ---------------- CURRENT STATUS ----------------
        status = result[8] if len(result) > 8 else "Pending"

        st.markdown("### 🚦 Current Status")

        if status == "Pending":
            st.warning("🟡 Pending")
        elif status == "In Progress":
            st.info("🔵 In Progress")
        elif status == "Solved":
            st.success("🟢 Solved")
        else:
            st.error("Unknown")

        # ---------------- MANUAL UPDATE (ONLY HERE) ----------------
        st.markdown("---")
        st.subheader("✏️ Update Status (Manual)")

        new_status = st.selectbox(
            "Change Status",
            ["Pending", "In Progress", "Solved"]
        )

        if st.button("Update Status"):

            conn = sqlite3.connect("disasterguard.db", check_same_thread=False)
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE reports
                SET status = ?
                WHERE tracking_id = ?
            """, (new_status, track_id))

            conn.commit()
            conn.close()

            st.success("Status updated successfully!")
            st.rerun()

    else:
        st.error("Not found")