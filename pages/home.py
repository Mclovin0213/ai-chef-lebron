import streamlit as st
import auth
from firebase_utils import initialize_firebase

auth_instance, database_instance = initialize_firebase()

def show():
    if auth.is_authenticated():
        st.title("🏠 Home")
        st.write(f"Hello, {st.session_state.get('username', 'User')}!")
        st.write("Welcome to your AI Recipe Helper.")

    else:
        st.warning("Please login to view the Home page.")
        auth.show_login_signup_form()

show()