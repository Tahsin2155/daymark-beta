# ============================================================================
# DATABASE MODULE (FIRESTORE)
# ============================================================================
# This file handles all database operations using Firebase Firestore.
#
# WHAT IS FIRESTORE?
# - A cloud-hosted NoSQL database by Google
# - Data is organized in collections (like folders) and documents (like files)
# - Each document contains fields (like a dictionary)
#
# OUR DATABASE STRUCTURE:
# users/
#   └── {user_id}/                    ← Each user has their own folder
#       ├── settings/
#       │   └── profile               ← User settings (name, email, etc.)
#       └── {YYYY-MM}/                ← One folder per month (e.g., "2025-12")
#           ├── habits                ← Habit data for the month
#           ├── journal               ← Journal entries for the month
#           └── tasks                 ← Tasks for each day
#
# CACHING:
# We use @st.cache_resource to avoid reinitializing Firebase on every rerun.
# This makes the app much faster!
# ============================================================================

import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st


# ----------------------------------------------------------------------------
# DATABASE CONNECTION
# ----------------------------------------------------------------------------

@st.cache_resource  # Cache this so it only runs once (not on every rerun)
def get_db():
    """
    Initialize Firebase and return a Firestore database client.
    
    This function:
    1. Loads credentials from Streamlit secrets
    2. Initializes the Firebase app
    3. Returns a Firestore client for database operations
    
    Returns:
        google.cloud.firestore.Client: The Firestore database client
    """
    # Load the service account credentials from secrets
    # (These are stored in .streamlit/secrets.toml)
    key_dict = dict(st.secrets["service_account"])
    
    # Create a Certificate object from the credentials
    cred = credentials.Certificate(key_dict)
    
    # Initialize the Firebase Admin SDK
    firebase_admin.initialize_app(cred)
    
    # Return the Firestore client (this is what we use to read/write data)
    return firestore.client()


# ----------------------------------------------------------------------------
# USER SETTINGS FUNCTIONS
# ----------------------------------------------------------------------------
# These functions handle the user's profile settings (name, email, etc.)
# Settings are stored at: users/{uid}/settings/profile

def get_user_settings(uid):
    """
    Load a user's settings from the database.
    
    Args:
        uid (str): The user's unique Firebase ID
    
    Returns:
        dict: The user's settings, or empty dict if none exist
    """
    db = get_db()
    
    # Navigate to the user's profile document
    doc = db.collection('users').document(uid).collection('settings').document('profile').get()
    
    # Return the data if it exists, otherwise return empty dict
    if doc.exists:
        return doc.to_dict()
    return {}


def update_user_settings(uid, settings_data):
    """
    Save or update a user's settings in the database.
    
    Args:
        uid (str): The user's unique Firebase ID
        settings_data (dict): The settings to save (e.g., {"name": "John", "email": "..."})
    
    Note: merge=True means existing fields are kept, only specified fields are updated
    """
    db = get_db()
    
    # Save the settings (merge=True preserves any fields not in settings_data)
    db.collection('users').document(uid).collection('settings').document('profile').set(
        settings_data, 
        merge=True
    )


# ----------------------------------------------------------------------------
# MONTHLY DATA FUNCTIONS
# ----------------------------------------------------------------------------
# These functions load and save all the data for a specific month.
# We use a "local-first" approach:
#   1. Load all data for a month into memory
#   2. User edits happen in memory (fast!)
#   3. Save everything back when user clicks "Save" or changes month

def load_month_data(uid, month_key):
    """
    Load all habits, journal entries, and tasks for a specific month.
    
    Uses batch get_all() for parallel fetching (single round-trip to Firestore).
    
    Args:
        uid (str): The user's unique Firebase ID
        month_key (str): The month to load, formatted as "YYYY-MM" (e.g., "2025-12")
    
    Returns:
        tuple: (habits_dict, journal_dict, tasks_dict)
        
    Example return:
        habits = {"Exercise": {"1": True, "2": False, ...}}
        journal = {"1": "Dear diary...", "15": "Today was great!"}
        tasks = {"1": {"Buy milk": True, "Call mom": False}}
    """
    db = get_db()
    
    # Create references to the three documents we need
    user_month_ref = db.collection('users').document(uid).collection(month_key)
    refs = [
        user_month_ref.document('habits'),
        user_month_ref.document('journal'),
        user_month_ref.document('tasks'),
    ]
    
    # Fetch all three documents in a single round-trip (parallel read)
    docs = db.get_all(refs)
    
    # Convert documents to dictionaries (or empty dict if they don't exist)
    # get_all() returns documents in the same order as refs
    results = [doc.to_dict() if doc.exists else {} for doc in docs]
    
    return results[0], results[1], results[2]


def save_month_data(uid, month_key, habits_data, journal_data, tasks_data):
    """
    Save all habits, journal entries, and tasks for a specific month.
    
    Uses a Firestore "batch" to save all three documents in one operation.
    This is faster and ensures all data is saved together (atomic write).
    
    Args:
        uid (str): The user's unique Firebase ID
        month_key (str): The month to save, formatted as "YYYY-MM"
        habits_data (dict): All habits for the month
        journal_data (dict): All journal entries for the month
        tasks_data (dict): All tasks for the month
    """
    db = get_db()
    
    # Create a batch - this lets us write multiple documents at once
    batch = db.batch()
    
    # Create references to where we'll save the data
    habits_ref = db.collection('users').document(uid).collection(month_key).document('habits')
    journal_ref = db.collection('users').document(uid).collection(month_key).document('journal')
    tasks_ref = db.collection('users').document(uid).collection(month_key).document('tasks')
    
    # Add each document to the batch
    # We use set() without merge=True to completely overwrite the documents
    # This ensures that deleted habits/tasks are actually removed
    batch.set(habits_ref, habits_data)
    batch.set(journal_ref, journal_data)
    batch.set(tasks_ref, tasks_data)
    
    # Execute all writes at once
    batch.commit()