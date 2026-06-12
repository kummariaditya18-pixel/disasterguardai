import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("disasterguard.db", check_same_thread=False)
cursor = conn.cursor()

# ---------------- SAFE TABLE ENSURE ----------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tracking_id TEXT,
    name TEXT,
    location TEXT,
    disaster_type TEXT,
    severity TEXT,
    description TEXT,
    image_path TEXT,
    status TEXT DEFAULT 'Pending'
)
""")

conn.commit()

# ---------------- SAFE DATA FETCH (NO PANDAS CRASH) ----------------
try:
    cursor.execute("SELECT * FROM reports ORDER BY id DESC")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(rows, columns=columns)

except Exception as e:
    st.error(f"Database error: {e}")
    df = pd.DataFrame()