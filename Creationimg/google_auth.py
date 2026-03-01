# google_auth.py
import streamlit as st
from requests_oauthlib import OAuth2Session
import os

CLIENT_ID = st.secrets["google"]["client_id"]
CLIENT_SECRET = st.secrets["google"]["client_secret"]
REDIRECT_URI = st.secrets["google"]["redirect_uri"]  # e.g., "https://yourapp.streamlit.app/"
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USER_INFO_URL = "https://www.googleapis.com/oauth2/v1/userinfo"
SCOPE = ["openid", "email", "profile"]

def get_google_auth_url():
    oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
    authorization_url, _ = oauth.authorization_url(AUTHORIZATION_BASE_URL)
    return authorization_url

def handle_google_login():
    query_params = st.query_params
    if "code" in query_params:
        oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
        try:
            token = oauth.fetch_token(
                TOKEN_URL,
                client_secret=CLIENT_SECRET,
                code=query_params["code"],
            )
            # Fetch user info
            resp = oauth.get(USER_INFO_URL)
            if resp.ok:
                user_info = resp.json()
                st.session_state["logged_in"] = True
                st.session_state["user_name"] = user_info.get("name", "Google User")
                st.session_state["user_email"] = user_info.get("email")
                # Clear query params to avoid re-processing
                st.query_params.clear()
                return True
        except Exception as e:
            st.error(f"Google login failed: {e}")
    return False