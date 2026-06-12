import streamlit as st
from utils.lang import translations
import pandas as pd

# ---------------- LANGUAGE ----------------
lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations[lang]

# ---------------- SAFE ACCESS FUNCTION ----------------
def tr(key, fallback):
    return t.get("menu", {}).get(key, fallback)

# ---------------- TITLE (FIXED ONLY) ----------------
st.title("🗺️ " + tr("map", "Live Map"))

# ---------------- SAMPLE DATA (UNCHANGED IDEA) ----------------
data = pd.DataFrame(
    {
        "lat": [17.3850, 16.5062],
        "lon": [78.4867, 80.6480],
        "city": ["Hyderabad", "Vijayawada"]
    }
)

st.map(data)

st.info("Live Map Loaded Successfully 🚀")