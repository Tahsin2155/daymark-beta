import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# Firestore structure used by this app
# - users/{uid}/settings/profile
# - users/{uid}/{YYYY-MM}/habits
# - users/{uid}/{YYYY-MM}/journal

# This function connects to the database
def get_db():
    # Check if we are already connected to avoid errors
    if not firebase_admin._apps:
        # Load the credentials from secrets
        key_dict = dict(st.secrets["service_account"])
        
        # Create the credential object
        cred = credentials.Certificate(key_dict)
        
        # Initialize the app
        firebase_admin.initialize_app(cred)
    
    return firestore.client()

# --- Settings (User Profile) ---

def get_user_settings(uid):
    db = get_db()
    # Path: users/{uid}/settings/profile
    doc = db.collection('users').document(uid).collection('settings').document('profile').get()
    if doc.exists:
        return doc.to_dict()
    return {}

def update_user_settings(uid, settings_data):
    db = get_db()
    # Path: users/{uid}/settings/profile
    db.collection('users').document(uid).collection('settings').document('profile').set(settings_data, merge=True)


# --- Batch Operations (Local-First Architecture) ---
def load_month_data(uid, month_key):
    """Fetches both habits and journal for a specific month in one go.
    Path: users/{uid}/{month_key}/habits and users/{uid}/{month_key}/journal
    """
    db = get_db()
    # Path: users/{uid}/{YYYY-MM}/habits and users/{uid}/{YYYY-MM}/journal
    habits_ref = db.collection('users').document(uid).collection(month_key).document('habits')
    journal_ref = db.collection('users').document(uid).collection(month_key).document('journal')
    
    habits_doc = habits_ref.get()
    journal_doc = journal_ref.get()
    
    habits_data = habits_doc.to_dict() if habits_doc.exists else {}
    journal_data = journal_doc.to_dict() if journal_doc.exists else {}
    
    return habits_data, journal_data

def save_month_data(uid, month_key, habits_data, journal_data):
    """Saves entire month's state to Firestore.
    Path: users/{uid}/{month_key}/habits and users/{uid}/{month_key}/journal
    """
    db = get_db()
    batch = db.batch()
    
    # Path: users/{uid}/{YYYY-MM}/habits and users/{uid}/{YYYY-MM}/journal
    habits_ref = db.collection('users').document(uid).collection(month_key).document('habits')
    journal_ref = db.collection('users').document(uid).collection(month_key).document('journal')
    
    # Overwrite habits (merge=False) to ensure deletions persist
    batch.set(habits_ref, habits_data) 
    
    # Overwrite journal (merge=False) to ensure we save exactly what is in session state
    # (Since we load everything, editing locally, and saving back, overwrite is safe and correct)
    batch.set(journal_ref, journal_data)
    
    batch.commit()
