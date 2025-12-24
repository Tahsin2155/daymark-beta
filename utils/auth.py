# ============================================================================
# AUTHENTICATION MODULE
# ============================================================================
# This file handles user login and signup using Firebase Authentication.
#
# HOW IT WORKS:
# - Firebase provides a REST API for authentication
# - We send the user's email/password to Firebase
# - Firebase validates it and returns a token (if successful)
# - The token proves the user is logged in
#
# FIREBASE AUTH URLS:
# - Login:  .../accounts:signInWithPassword
# - Signup: .../accounts:signUp
# ============================================================================

import requests  # Library for making HTTP requests to APIs
import streamlit as st  # Used to access secrets (API key)


def login_user(email, password):
    """
    Authenticate an existing user with Firebase.
    
    Args:
        email (str): The user's email address
        password (str): The user's password
    
    Returns:
        dict: Firebase response containing 'idToken' if successful,
              or 'error' with details if failed
    """
    # Get the Firebase API key from Streamlit secrets
    # (Secrets are stored in .streamlit/secrets.toml or Streamlit Cloud)
    api_key = st.secrets["firebase"]["apiKey"]

    # Firebase REST API endpoint for signing in
    url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}'

    # The data to send to Firebase
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True  # We want an ID token back
    }

    # Send a POST request to Firebase with the login credentials
    response = requests.post(url, json=payload)

    # Return the JSON response (contains idToken on success, error on failure)
    return response.json()


def signup_user(email, password):
    """
    Create a new user account with Firebase.
    
    Args:
        email (str): The new user's email address
        password (str): The new user's password (Firebase requires 6+ characters)
    
    Returns:
        dict: Firebase response containing 'idToken' if successful,
              or 'error' with details if failed (e.g., email already exists)
    """
    api_key = st.secrets["firebase"]["apiKey"]
    
    # Different endpoint for signup: ":signUp" instead of ":signInWithPassword"
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    response = requests.post(url, json=payload)
    return response.json()
