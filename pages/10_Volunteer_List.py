import streamlit as st
from backend.database import get_volunteers
from utils.lang import translations

lang = st.session_state.get("lang", "English")

if lang not in translations:
    lang = "English"

t = translations[lang]

st.title("👥 " + t["menu"]["vol_list"])

volunteers = get_volunteers()

if volunteers:
    for volunteer in volunteers:
        _vid, name, phone, skill = volunteer

        with st.container():
            st.write(f"👤 {name}")
            st.write(f"📞 {phone}")
            st.write(f"🛠 {skill}")

            st.markdown("---")

else:
    st.info(t.get("no_volunteers", "No volunteers registered yet."))
