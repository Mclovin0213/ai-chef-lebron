import streamlit as st
import auth
from firebase_utils import initialize_firebase

auth_instance, database_instance = initialize_firebase()

# --- Authentication Logic ---
if not auth.is_authenticated():
    st.title("Welcome to Lebron's AI Recipe Helper!")
    st.info("Please login or sign up to continue.")
    auth.show_login_signup_form()
else:
    # --- Authenticated App Content ---
    st.sidebar.title("Navigation")
    st.sidebar.write(f"Welcome, {st.session_state.get('username', 'User')}!")
    if st.sidebar.button("Logout"):
        auth.logout()