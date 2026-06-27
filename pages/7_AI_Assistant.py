import streamlit as st
from utils.lang import translations

# ---------------- LANGUAGE ----------------
lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations[lang]

# ---------------- TITLE ----------------
st.title("🤖 " + t["menu"]["assistant"])

# ---------------- QUESTION INPUT ----------------
question = st.text_input("Ask a disaster-related question")

if question:
    q = question.lower()

    if "flood" in q:
        st.success(
            f"""
{t["menu"]["map"]} Safety Tips:

• Move to higher ground
• Avoid walking through flood water
• Keep emergency supplies ready
• Follow official alerts
"""
        )

    elif "fire" in q:
        st.success(
            """
Fire Safety Tips:

• Leave the building immediately
• Use stairs, not elevators
• Call emergency services
• Stay low if there is smoke
"""
        )

    elif "earthquake" in q:
        st.success(
            """
Earthquake Safety Tips:

• Drop, Cover and Hold On
• Stay away from windows
• Move to open space after shaking stops
"""
        )

    else:
        st.info("Please ask about flood, fire, or earthquake.")
