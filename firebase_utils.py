import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import json

@st.cache_resource
def initialize_firebase():
    firebase_config = {
        "apiKey": st.secrets["firebase_client_config"]["apiKey"],
        "authDomain": st.secrets["firebase_client_config"]["authDomain"],
        "databaseURL": st.secrets["firebase_client_config"]["databaseURL"],
        "projectId": st.secrets["firebase_client_config"]["projectId"],
        "storageBucket": st.secrets["firebase_client_config"]["storageBucket"],
        "messagingSenderId": st.secrets["firebase_client_config"]["messagingSenderId"],
        "appId": st.secrets["firebase_client_config"]["appId"],
    }

    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()

    try:
        service_account_info = st.secrets["firebase_admin_sdk"]
        service_account_json = json.loads(json.dumps(service_account_info))
        cred = credentials.Certificate(service_account_json)
    except Exception:
        st.error("Could not load Firebase Admin service account from secrets.")
        st.stop()

    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    database = firestore.client()

    return auth, database