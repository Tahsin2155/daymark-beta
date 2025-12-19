import requests
import streamlit as st

# This function sends the email/password to Firebase and returns the response
def login_user(email, password):
    # We get the API key from the secrets file we just made
    api_key = st.secrets["firebase"]["apiKey"]

    # This is the specific URL for the Firebase authentication API
    url = f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}'

    # the data we send to Firebase
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    # Send the request to Firebase
    response = requests.post(url, json=payload)

    # Return the response
    return response.json()

# Function to sign up a new user
def signup_user(email, password):
    api_key = st.secrets["firebase"]["apiKey"]
    
    # Note the different URL here: ":signUp" instead of ":signInWithPassword"
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    response = requests.post(url, json=payload)
    return response.json()
