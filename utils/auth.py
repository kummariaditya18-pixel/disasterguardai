import streamlit as st

# 🔐 HARD-CODED ADMIN (you can change this)
ADMIN_CREDENTIALS = {"admin": "admin123"}


def login(username, password):
    if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
        st.session_state["admin_logged_in"] = True
        st.session_state["admin_user"] = username
        return True
    return False


def logout():
    st.session_state["admin_logged_in"] = False
    st.session_state["admin_user"] = None


def is_admin():
    return st.session_state.get("admin_logged_in", False)
