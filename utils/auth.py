"""
Authentication Page for DayMark
===============================
Handles user login and signup with Firebase email verification.

INTEGRATION NOTES:
------------------
To integrate this into the main app (streamlit_app.py), you can either:
1. Import and call show_auth_page() from this module
2. Copy the UI section into your main app's auth flow

FUNCTIONS TO MOVE TO utils/auth.py:
-----------------------------------
- send_verification_email()  -> Sends Firebase email verification
- get_account_info()         -> Retrieves user account details from Firebase
- is_email_verified()        -> Checks if user's email is verified

These functions are Firebase auth-related and belong with login_user/signup_user.
"""

import datetime
import re
import requests
import streamlit as st
from zoneinfo import ZoneInfo
from utils import db


# =============================================================================
# CONSTANTS
# =============================================================================
MIN_PASSWORD_LENGTH = 8  # Firebase minimum requirement
IST = ZoneInfo("Asia/Kolkata")  # App timezone

# Pre-compiled email regex (avoids recompiling on every validation)
_EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


# =============================================================================
# CACHED API KEY & HTTP SESSION
# =============================================================================
@st.cache_data(ttl=3600)  # Cache for 1 hour (API key doesn't change)
def _get_firebase_api_key() -> str:
    """Get Firebase API key from secrets (cached to avoid repeated lookups)."""
    return st.secrets["firebase"]["apiKey"]


@st.cache_resource  # Singleton HTTP session for connection pooling
def _get_http_session() -> requests.Session:
    """Get a reusable HTTP session for connection pooling."""
    session = requests.Session()
    # Set default timeout and headers
    session.headers.update({"Content-Type": "application/json"})
    return session


# =============================================================================
# HELPER FUNCTIONS
# TODO: Move these to utils/auth.py for better organization
# =============================================================================
def login_user(email: str, password: str) -> dict:
    """
    Authenticate an existing user with Firebase (email/password).

    Args:
        email: The user's email address
        password: The user's password

    Returns:
        dict: Firebase response JSON. On success includes 'idToken', 'localId',
              'refreshToken'. On failure includes 'error' details.
    """
    api_key = _get_firebase_api_key()
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True,
    }
    resp = _get_http_session().post(url, json=payload, timeout=10)
    return resp.json()


def signup_user(email: str, password: str) -> dict:
    """
    Create a new user account with Firebase (email/password).

    Args:
        email: The user's email address
        password: The user's password (Firebase requires 6+ characters)

    Returns:
        dict: Firebase response JSON. On success includes 'idToken', 'localId',
              'refreshToken'. On failure includes 'error' details.
    """
    api_key = _get_firebase_api_key()
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True,
    }
    resp = _get_http_session().post(url, json=payload, timeout=10)
    return resp.json()

def send_verification_email(id_token: str) -> dict:
    """
    Send Firebase's built-in verification email.
    
    Args:
        id_token: The user's Firebase ID token (from login/signup response)
    
    Returns:
        dict: {"email": "..."} on success, {"error": "..."} on failure
    """
    try:
        api_key = _get_firebase_api_key()
    except KeyError:
        return {"error": "Firebase API key not configured in secrets"}
    
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={api_key}"
    payload = {"requestType": "VERIFY_EMAIL", "idToken": id_token}
    
    try:
        resp = _get_http_session().post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception:
        return {"error": "Failed to send verification email"}


def get_account_info(id_token: str) -> dict:
    """
    Retrieve account info from Firebase for the given ID token.
    
    Args:
        id_token: The user's Firebase ID token
    
    Returns:
        dict: {"users": [...]} on success, {"error": "..."} on failure
    """
    try:
        api_key = _get_firebase_api_key()
    except KeyError:
        return {"error": "Firebase API key not configured in secrets"}
    
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={api_key}"
    payload = {"idToken": id_token}
    
    try:
        resp = _get_http_session().post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.exceptions.Timeout:
        return {"error": "Request timed out. Please try again."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}
    except Exception:
        return {"error": "Failed to retrieve account info"}


def is_email_verified(id_token: str) -> tuple[bool, str | None]:
    """
    Check if the user's email is verified.
    
    Args:
        id_token: The user's Firebase ID token
    
    Returns:
        tuple: (is_verified: bool, error_message: str | None)
    """
    acct = get_account_info(id_token)
    
    if acct.get("error"):
        return False, acct["error"]
    
    users = acct.get("users", [])
    if not users:
        return False, "Failed to retrieve account info"
    
    return users[0].get("emailVerified", False), None


def is_valid_email(email: str) -> bool:
    """Validate email format using pre-compiled regex."""
    return bool(_EMAIL_PATTERN.match(email))


def validate_inputs(email: str, password: str, is_signup: bool = False) -> tuple[bool, str]:
    """
    Validate user inputs before sending to Firebase.
    
    Args:
        email: User's email address
        password: User's password
        is_signup: Whether this is a signup (applies stricter validation)
    
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not email or not email.strip():
        return False, "Please enter your email address"
    
    if not is_valid_email(email.strip()):
        return False, "Please enter a valid email address"
    
    if not password:
        return False, "Please enter your password"
    
    if is_signup and len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters"
    
    return True, ""


def create_user_settings(email: str, password: str) -> dict:
    """
    Create initial settings for a new user.
    
    Args:
        email: The user's email address
        password: The user's password (stored for account recovery reference)
    
    Returns:
        dict: Default settings data
    """
    return {
        "email": email,
        "name": "",
        "password": password,
        "date_of_account_creation": datetime.datetime.now(IST).strftime("%Y-%m-%d"),
        "reflection_questions": ""
    }


def complete_login(user_data: dict) -> None:
    """
    Complete the login process by setting session state and redirecting.
    
    Args:
        user_data: The Firebase user data (must contain 'localId' and 'idToken')
    """
    st.session_state.user = user_data
    st.session_state.settings = db.get_user_settings(user_data["localId"])
    # Clear any pending verification states
    st.session_state.pending_verification = None
    st.session_state.unverified_login = None
    st.rerun()


def clear_verification_states() -> None:
    """Clear all verification-related session states."""
    st.session_state.pending_verification = None
    st.session_state.unverified_login = None


# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================
def init_session_state() -> None:
    """Initialize all required session state variables (only if missing)."""
    # Early return if already initialized (check one key as proxy)
    if "auth_mode" in st.session_state:
        return
    
    st.session_state.setdefault("pending_verification", None)
    st.session_state.setdefault("unverified_login", None)
    st.session_state.setdefault("auth_mode", "Login")


# =============================================================================
# UI COMPONENTS
# =============================================================================

def render_verification_section(verification_data: dict, section_key: str) -> None:
    """
    Render the email verification UI section.
    
    Args:
        verification_data: Dict containing 'idToken' and 'localId'
        section_key: Unique key prefix for buttons (e.g., 'login', 'signup')
    """
    st.divider()
    st.subheader("📧 Email Verification Required")
    st.info("Please check your inbox (and spam folder) for the verification email.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Resend verification email", key=f"resend_{section_key}"):
            with st.spinner("Sending..."):
                resp = send_verification_email(verification_data["idToken"])
            if resp.get("error"):
                st.error(resp["error"])
            else:
                st.success("✅ Verification email sent! Check your inbox.")
    
    with col2:
        if st.button("✓ I've verified — continue", key=f"check_{section_key}"):
            with st.spinner("Checking..."):
                verified, error = is_email_verified(verification_data["idToken"])
            
            if error:
                st.error(error)
            elif verified:
                st.success("✅ Email verified! Signing you in...")
                complete_login(verification_data)
            else:
                st.warning("⚠️ Email not yet verified. Please click the link in the email.")
    
    # Option to cancel and go back
    if st.button("← Back to login", key=f"back_{section_key}"):
        clear_verification_states()
        st.rerun()


def handle_login(email: str, password: str) -> None:
    """
    Handle the login flow.
    
    Args:
        email: User's email address
        password: User's password
    """
    # Validate inputs
    is_valid, error_msg = validate_inputs(email, password)
    if not is_valid:
        st.error(error_msg)
        return
    
    # Attempt login
    with st.spinner("Signing in..."):
        result = login_user(email.strip(), password)
    
    if "idToken" not in result:
        # Parse Firebase error messages into user-friendly format
        error = result.get("error", {})
        message = error.get("message", "An error occurred") if isinstance(error, dict) else str(error)
        
        # Make common errors more user-friendly
        friendly_messages = {
            "EMAIL_NOT_FOUND": "No account found with this email address",
            "INVALID_PASSWORD": "Incorrect password",
            "INVALID_LOGIN_CREDENTIALS": "Invalid email or password",
            "USER_DISABLED": "This account has been disabled",
            "TOO_MANY_ATTEMPTS_TRY_LATER": "Too many failed attempts. Please try again later",
        }
        st.error(friendly_messages.get(message, message))
        return
    
    # Check email verification status
    verified, error = is_email_verified(result["idToken"])
    
    if error:
        st.error(error)
        return
    
    if verified:
        st.success("✅ Login successful!")
        complete_login(result)
    else:
        st.warning("⚠️ Please verify your email before logging in.")
        st.session_state.unverified_login = {
            "idToken": result["idToken"],
            "localId": result["localId"],
        }
        st.rerun()


def handle_signup(email: str, password: str) -> None:
    """
    Handle the signup flow.
    
    Args:
        email: User's email address
        password: User's password
    """
    # Validate inputs with signup rules
    is_valid, error_msg = validate_inputs(email, password, is_signup=True)
    if not is_valid:
        st.error(error_msg)
        return
    
    # Attempt signup
    with st.spinner("Creating your account..."):
        result = signup_user(email.strip(), password)
    
    if "idToken" not in result:
        error = result.get("error", {})
        message = error.get("message", "An error occurred") if isinstance(error, dict) else str(error)
        
        friendly_messages = {
            "EMAIL_EXISTS": "An account with this email already exists",
            "WEAK_PASSWORD": f"Password must be at least {MIN_PASSWORD_LENGTH} characters",
            "INVALID_EMAIL": "Please enter a valid email address",
            "OPERATION_NOT_ALLOWED": "Email/password signup is disabled",
        }
        st.error(friendly_messages.get(message, message))
        return
    
    st.success("🎉 Account created successfully!")
    
    # Create user settings in database
    settings_data = create_user_settings(email.strip(), password)
    db.update_user_settings(result["localId"], settings_data)
    st.session_state.settings = settings_data
    
    # Send verification email
    with st.spinner("Sending verification email..."):
        send_resp = send_verification_email(result["idToken"])
    
    if send_resp.get("error"):
        st.error(f"Could not send verification email: {send_resp['error']}")
        st.info("You can request a new verification email after logging in.")
    else:
        st.info("📧 A verification email has been sent. Please verify to continue.")
    
    # Store for verification flow
    st.session_state.pending_verification = {
        "idToken": result["idToken"],
        "localId": result["localId"],
    }
    st.rerun()


# =============================================================================
# LEGACY AUTH (from main.py - no email verification)
# =============================================================================

def show_auth_page_legacy() -> None:
    """
    Original authentication page WITHOUT email verification.
    
    Copied from main.py for reference/fallback.
    Use show_auth_page() instead for the version with email verification.
    """
    # Check if user is logged in (user will be None if not logged in)
    if st.session_state.get("user"):
        return
    
    st.title("Welcome to DayMark!")
    st.subheader("🔐 Sign in to continue")
    
    # Radio button lets user choose between Login and Sign Up
    mode = st.radio("Choose an option", ["Login", "Sign Up"], horizontal=True)

    # Create a form - forms group inputs and submit together
    with st.form("auth_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        # When the submit button is clicked, this block runs
        if st.form_submit_button(mode):
            # Call the appropriate auth function based on mode
            if mode == "Login":
                result = login_user(email, password)
            else:
                result = signup_user(email, password)
                # For new users, create their initial settings
                settings_data = {
                    "email": email,
                    "name": "",
                    "date_of_account_creation": datetime.datetime.now(IST).strftime("%Y-%m-%d"),
                    "reflection_questions": ""
                }

            # Check if authentication was successful
            # Firebase returns 'idToken' when login/signup works
            if 'idToken' in result:
                st.success(f"{mode} Success!")
                st.session_state.user = result
                
                # Load or create user settings
                if mode == 'Login':
                    st.session_state.settings = db.get_user_settings(result['localId'])
                else:
                    db.update_user_settings(result['localId'], settings_data)
                    st.session_state.settings = settings_data
                
                st.rerun()
            else:
                # Login/signup failed - show the error message from Firebase
                st.error(result.get("error", {}).get("message", "An error occurred"))

    st.stop()


# =============================================================================
# MAIN AUTH PAGE (with email verification)
# =============================================================================

def show_auth_page() -> None:
    """
    Display the authentication page.
    
    This function can be called from streamlit_app.py to show the auth UI.
    """
    init_session_state()
    
    # If user is already logged in, don't show auth page
    if "user" in st.session_state and st.session_state.user:
        return
    st.set_page_config(page_title="DayMark - Login", layout="centered")
    st.title("Welcome to DayMark!")
    st.subheader("🔐 Sign in to continue")
    
    # Check for pending verification states BEFORE showing the form
    if st.session_state.unverified_login:
        render_verification_section(st.session_state.unverified_login, "login")
        st.stop()
    
    if st.session_state.pending_verification:
        render_verification_section(st.session_state.pending_verification, "signup")
        st.stop()
    
    # Auth mode selection
    mode = st.radio(
        "Choose an option",
        ["Login", "Sign Up"],
        horizontal=True,
        key="auth_mode_radio"
    )
    
    # Clear verification states when switching modes
    if st.session_state.auth_mode != mode:
        clear_verification_states()
        st.session_state.auth_mode = mode
    
    # Auth form
    with st.form("auth_form", clear_on_submit=False):
        email = st.text_input(
            "Email",
            placeholder="you@example.com",
            autocomplete="email"
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            autocomplete="current-password" if mode == "Login" else "new-password"
        )
        
        # Show password requirements for signup
        if mode == "Sign Up":
            st.caption(f"Password must be at least {MIN_PASSWORD_LENGTH} characters")
        
        submit_label = "🔑 Login" if mode == "Login" else "✨ Create Account"
        submitted = st.form_submit_button(submit_label, width='stretch')
        
        if submitted:
            if mode == "Login":
                handle_login(email, password)
            else:
                handle_signup(email, password)
    
    # Footer links (optional - for terms, privacy, etc.)
    st.divider()
    st.caption("By continuing, you agree to our Terms of Service and Privacy Policy.")
    
    # Stop execution here - don't let the rest of main.py run
    st.stop()


# =============================================================================
# ENTRY POINT
# =============================================================================

# Run the auth page when this file is executed directly or imported as a page
if __name__ == "__main__" or "user" not in st.session_state:
    show_auth_page()
    st.stop()
