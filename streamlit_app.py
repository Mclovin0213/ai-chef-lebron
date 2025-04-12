import streamlit as st
import pyrebase
import firebase_admin
import json
from firebase_admin import credentials, firestore
from firebaseconfig import firebaseConfig

# client_config = st.secrets["firebase_client_config"]
# admin_cred_dict = st.secrets["firebase_admin_sdk"]

# with open("/tmp/service_account.json", "w") as f:
#   json.dump(admin_cred_dict, f)

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# Initialize Firestore
if not firebase_admin._apps:
  cred = credentials.Certificate("/workspaces/ai-chef-lebron/ai-chef-lebron-firebase-adminsdk-fbsvc-6a5f73e9fc.json")
  firebase_admin.initialize_app(cred)

database = firestore.client()

st.title("Lebron's AI Recipe Helper")

choice = st.sidebar.selectbox("Login/Signup", ["Login", "Signup"])

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if choice == "Signup":
  username = st.text_input("Username")
  if st.button("Create Account"):
    try:
      user = auth.create_user_with_email_and_password(email, password)
      st.success("Account created successfully")
      database.collection("users").document(user['localId']).set({
        "email": email,
        "username": username,
      })
    except Exception as e:
      st.error(f"Error: {e}")

elif choice == "Login":
  if st.button("Login"):
    try:
      user = auth.sign_in_with_email_and_password(email, password)
      st.success("Login Successful!")
      st.session_state['user'] = user
    except Exception as e:
      st.error(f"Error: {e}")

# Display user info if logged in
if "user" in st.session_state:
    st.subheader("Welcome!")
    user = st.session_state['user']
    user_info = database.collection("users").document(user['localId']).get().to_dict()
    st.write(f"Username: {user_info['username']}")
    st.write(f"Email: {user_info['email']}")
    if st.button("Logout"):
        st.session_state.pop("user", None)
        st.success("Logged out successfully.")
        st.rerun()


  






