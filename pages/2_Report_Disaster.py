import streamlit as st
import sqlite3
import datetime
import os
import uuid

from utils.lang import translations

# ---------------- LANGUAGE ----------------
lang = st.session_state.get("lang", "English")
t = translations.get(lang, translations["English"])

st.title("🚨 " + t["menu"].get("report", "Report Disaster"))
st.write(t.get("welcome", "Report disasters quickly"))

# ---------------- DB ----------------
conn = sqlite3.connect("disasterguard.db", check_same_thread=False)
cursor = conn.cursor()

# ---------------- CREATE TABLE (SAFE) ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    tracking_id TEXT PRIMARY KEY,
    name TEXT,
    location TEXT,
    disaster_type TEXT,
    severity TEXT,
    description TEXT,
    image_path TEXT,
    created_at TEXT
)
""")
conn.commit()

# ---------------- DISASTER OPTIONS ----------------
disasters = [
    "Flood 🌊",
    "Earthquake 🌍",
    "Cyclone 🌪️",
    "Storm ⛈️",
    "Fire 🔥",
    "Landslide ⛰️",
    "Tsunami 🌊",
    "Other ⚠️"
]

severities = [
    "Low 🟢",
    "Medium 🟡",
    "High 🔴",
    "Critical 🚨"
]

# ---------------- FORM ----------------
with st.form("report_form", clear_on_submit=True):

    name = st.text_input("👤 Name")
    location = st.text_input("📍 Location")

    disaster = st.selectbox("🌪️ Disaster Type", disasters)
    severity = st.selectbox("⚠️ Severity", severities)

    description = st.text_area("📝 Description")

    image = st.file_uploader("📷 Upload Image (Optional)", type=["jpg", "jpeg", "png"])

    submit = st.form_submit_button("🚨 Submit Report")

# ---------------- SAVE LOGIC (100% SAFE) ----------------
if submit:
    if not name or not location or not description:
        st.error("❌ Please fill all required fields")
    else:
        try:
            tracking_id = str(uuid.uuid4())[:8]

            # ---------------- IMAGE SAVE ----------------
            image_path = None
            if image:
                os.makedirs("uploads", exist_ok=True)
                image_path = f"uploads/{tracking_id}_{image.name}"
                with open(image_path, "wb") as f:
                    f.write(image.getbuffer())

            # ---------------- SAFE INSERT (NO COLUMN ERROR EVER) ----------------
            try:
                created_at = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                cursor.execute("""
                    INSERT INTO reports (
                        tracking_id, name, location,
                        disaster_type, severity,
                        description, image_path, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    tracking_id,
                    name,
                    location,
                    disaster,
                    severity,
                    description,
                    image_path,
                    created_at
                ))

            except sqlite3.OperationalError:
                # fallback for OLD DB (no created_at column)
                cursor.execute("""
                    INSERT INTO reports (
                        tracking_id, name, location,
                        disaster_type, severity,
                        description, image_path
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    tracking_id,
                    name,
                    location,
                    disaster,
                    severity,
                    description,
                    image_path
                ))

            conn.commit()

            st.success("✅ Report submitted successfully!")
            st.info(f"🆔 Tracking ID: {tracking_id}")

        except Exception as e:
            st.error(f"❌ Error saving report: {e}")

# ---------------- CLOSE ----------------
conn.close()