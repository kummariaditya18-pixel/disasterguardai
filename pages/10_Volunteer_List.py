import streamlit as st
import sqlite3

from utils.lang import translations

# ---------------- LANGUAGE ----------------
lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations[lang]

# ---------------- TITLE ----------------
st.title("👥 " + t["menu"]["vol_list"])

# ---------------- DATABASE ----------------
conn = sqlite3.connect("disasterguard.db")
cursor = conn.cursor()

try:
    cursor.execute("SELECT * FROM volunteers")
    volunteers = cursor.fetchall()

    if not volunteers:
        st.info("No volunteers registered.")
    else:

        for volunteer in volunteers:

            st.write(
                "Name: " + str(volunteer[1])
            )

            st.write(
                "Phone: " + str(volunteer[2])
            )

            st.write(
                "Skill: " + str(volunteer[3])
            )

            st.divider()

except Exception as e:
    st.error(f"Database Error: {e}")

finally:
    conn.close()