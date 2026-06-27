import streamlit as st
import sqlite3
import pandas as pd

from utils.lang import translations

# ---------------- LANGUAGE ----------------
lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations[lang]


def tr(key, fallback):
    return t.get("menu", {}).get(key, fallback)


# ---------------- TITLE ----------------
st.title("🗺️ " + tr("map", "Live Disaster Map"))

st.caption("Real-time disaster monitoring system")

st.markdown("---")

# ---------------- DATABASE ----------------
conn = sqlite3.connect("disasterguard.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute(
    """
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
"""
)

cursor.execute(
    """
SELECT location, disaster_type, severity
FROM reports
"""
)

rows = cursor.fetchall()
conn.close()

# ---------------- EMPTY STATE ----------------
if not rows:
    st.warning("No disaster data available yet")
    st.stop()

# ---------------- SAMPLE COORDINATES MAP ----------------
# (Since real geocoding not added yet)

city_coords = {
    "hyderabad": [17.3850, 78.4867],
    "vijayawada": [16.5062, 80.6480],
    "mumbai": [19.0760, 72.8777],
    "delhi": [28.7041, 77.1025],
    "chennai": [13.0827, 80.2707],
}

map_data = []

for loc, disaster, severity in rows:
    key = loc.lower().strip()

    if key in city_coords:
        lat, lon = city_coords[key]

        map_data.append(
            {
                "lat": lat,
                "lon": lon,
                "city": loc,
                "disaster": disaster,
                "severity": severity,
            }
        )

df = pd.DataFrame(map_data)

# ---------------- FILTER ----------------
st.subheader("🔍 Filter Map")

filter_type = st.selectbox("Select Severity", ["All", "High", "Medium", "Low"])

if filter_type != "All":
    df = df[df["severity"] == filter_type]

# ---------------- MAP DISPLAY ----------------
st.subheader("📍 Disaster Locations Map")

if not df.empty:
    st.map(df[["lat", "lon"]])

else:
    st.info("No data for selected filter")

# ---------------- SIDE INFO ----------------
st.markdown("---")
st.subheader("📊 Live Disaster Feed")

for _, row in df.iterrows():
    if row["severity"] == "High":
        st.error(f"🔥 {row['city']} - {row['disaster']} (HIGH RISK)")

    elif row["severity"] == "Medium":
        st.warning(f"⚠️ {row['city']} - {row['disaster']}")

    else:
        st.success(f"🟢 {row['city']} - {row['disaster']}")

st.markdown("---")

st.info("🗺️ Live Disaster Map System Active 🚀")
