from datetime import datetime
import streamlit as st

def show(database):
    st.subheader("Welcome!")
    user = st.session_state['user']
    user_info = database.collection("users").document(user['localId']).get().to_dict()
    st.write(f"Username: {user_info['username']}")
    st.write(f"Email: {user_info['email']}")
    if st.button("Logout"):
        st.session_state.pop("user", None)
        st.success("Logged out successfully.")
        st.rerun()
    
    entry_ref = database.collection("entries").document()
    entry_ref.set({
        "user_id": user['localId'],
        "email": user['email'],
        "date": datetime.now(),
        "content": user
    })