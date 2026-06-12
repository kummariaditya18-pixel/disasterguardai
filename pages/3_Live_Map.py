import streamlit as st
import pandas as pd
from utils.lang import translations

lang = st.session_state.get("lang", "English")
t = translations.get(lang, translations["English"])

st.title("🗺️ " + t["menu"]["map"])

data = pd.DataFrame(
    {
        "lat": [17.3850, 16.5062],
        "lon": [78.4867, 80.6480]
    }
)

st.map(data)