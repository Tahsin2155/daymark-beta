import streamlit as st
import datetime
import pandas as pd
from utils import auth, db, graphs

# NOTE:
# - Auth helpers live in `utils/auth.py`
# - Firestore read/write helpers live in `utils/db.py`
# - Analytics charts live in `utils/graphs.py`



# --------------------------------------------------
# Session initialization
# --------------------------------------------------

# Configure Streamlit page
st.set_page_config(
    page_title="DayMark",
    page_icon="📓",
    layout="wide"
)

# Track authenticated user in session
if "user" not in st.session_state:
    st.session_state.user = None


# --------------------------------------------------
# Authentication (Login / Signup)
# --------------------------------------------------

# If user is not logged in, show auth screen
if not st.session_state.user:

    st.title("Welcome to DayMark!")
    
    # ============================================
    # Email/Password Authentication
    # ============================================
    st.subheader("🔐 Sign in to continue")
    
    mode = st.radio("Choose an option", ["Login", "Sign Up"], horizontal=True)

    # Auth form
    with st.form("auth_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        # Button label matches selected mode
        if st.form_submit_button(mode, width='content'):
            if mode == "Login":
                result = auth.login_user(email, password)
            else:
                result = auth.signup_user(email, password)
                settings_data = {
                    "email": email,
                    "password": password,
                    "date_of_account_creation": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "reflection_questions": ""
                }

            # Successful Firebase auth returns an idToken
            if 'idToken' in result:
                st.success(f"{mode} Success!")
                st.session_state.user = result
                if mode == 'Login':
                    st.session_state.settings = db.get_user_settings(result['localId'])
                else:
                    db.update_user_settings(result['localId'], settings_data)
                    st.session_state.settings = settings_data
                st.rerun()
            else:
                # Display Firebase error message if available
                st.error(result.get("error", {}).get("message", "An error occurred"))

    # Stop app execution until user logs in
    st.stop()

# --------------------------------------------------
# Local in-memory state for habits & journal
# --------------------------------------------------

# Initialize per-session working data
if "data" not in st.session_state:
    st.session_state.data = {
        "habits": {},     # {habit_name: {"1": bool, "2": bool, ...}}
        "journal": {},    # {"1": "text", "2": "text", ...}
        "month_key": None
    }

st.title("DayMark")


# --------------------------------------------------
# Date selection & persistence
# --------------------------------------------------

hcol1,hcol2, hcol3 = st.columns([5,2,2])

# Date picker (used to determine month + journal day)
selected_date = hcol1.date_input("Select Date","today", max_value='today', min_value=(st.session_state.settings['date_of_account_creation']), label_visibility='collapsed')

# Month key used for grouping data (YYYY-MM)
current_month_key = selected_date.strftime("%Y-%m")

# Logged-in Firebase user id
user_id = st.session_state.user['localId']
def save():
    db.save_month_data(user_id, current_month_key, st.session_state.data["habits"], st.session_state.data["journal"])

def logout():
    # Callbacks can't rerun; set a flag and handle after UI
    st.session_state["__logout_requested__"] = True

# Manual save button
hcol2.button(
    "Save Changes", width='stretch',
    on_click=save)

hcol3.button('Logout', on_click=logout, width='stretch')

# Handle logout outside callback (rerun works here)
if st.session_state.get("__logout_requested__"):
    try:
        if st.session_state.get("data"):
            db.save_month_data(
                user_id,
                current_month_key,
                st.session_state.data.get("habits", {}),
                st.session_state.data.get("journal", {})
            )
    except Exception:
        pass
    # Clear state
    st.session_state.pop("habit_grid_df", None)
    st.session_state.pop("__logout_requested__", None)
    for key in ("user", "settings", "data"):
        st.session_state.pop(key, None)
    st.rerun()


st.info('Before Refreshing, Closing Tabs or Loging Out Click Save Changes')

# --------------------------------------------------
# Month change handling
# --------------------------------------------------

# If user switches months, persist old month and load new data
if current_month_key != st.session_state.data["month_key"]:

    # Save previous month's data before switching
    if st.session_state.data['month_key']:
        db.save_month_data(
            user_id,
            st.session_state.data['month_key'],
            st.session_state.data["habits"],
            st.session_state.data["journal"]
        )

    # Load habits & journal for the selected month
    habits, journals = db.load_month_data(user_id, current_month_key)

    st.session_state.data["habits"] = habits
    st.session_state.data["journal"] = journals
    st.session_state.data["month_key"] = current_month_key

    # Force UI refresh so editor resets correctly
    st.rerun()

# Short aliases for current working data
current_habit_data = st.session_state.data["habits"]
current_journal_data = st.session_state.data["journal"]

# --------------------------------------------------
# Main tabs
# --------------------------------------------------

habit, graph, journal = st.tabs(["Habits", "Analytics", "Journal"])

# ==================================================
# HABIT TRACKER TAB
# ==================================================

with habit:
    st.header("Habits")
    st.write(f"Viewing: **{current_month_key}**")

    # ------------------------------
    # Habit management UI
    # ------------------------------

    with st.popover("Manage Habits"):
        add, delete = st.tabs(["Add Habit", "Delete Habit"])

        # Add a new habit
        with add:
            new_habit_name = st.text_input("Enter New Habits Name", placeholder="Habit Name")


            if st.button("Add Habit"):
                if new_habit_name:
                    # Initialize habit with False for each day in the month (dict with "1" to "N" keys)
                    days_in_month = pd.Period(current_month_key).days_in_month
                    current_habit_data[new_habit_name] = {
                        str(d): False for d in range(1, days_in_month + 1)
                    }
                    # FORCE GRID REFRESH
                    if "habit_grid_df" in st.session_state:
                        del st.session_state.habit_grid_df
                    
                    st.success(f'Added {new_habit_name}')
                    st.rerun()
                else:
                    st.error("Please enter a habit name.")

        # Delete an existing habit
        with delete:
            habit_to_delete = st.selectbox(
                "Select Habit to Delete",
                current_habit_data.keys()
            )

            if st.button("Delete Habit", disabled=(False if habit_to_delete else True)):
                del current_habit_data[habit_to_delete]
                # FORCE GRID REFRESH
                if "habit_grid_df" in st.session_state:
                    del st.session_state.habit_grid_df
                
                st.rerun()


    # ------------------------------
    # Habit grid editor
    # ------------------------------

    # Show guidance if no habits exist
    if not current_habit_data:
        st.info("No habits found for this month. Please add some.")

    else:
        # Convert habits dict to DataFrame (Habits = rows, Days = columns)
        df = pd.DataFrame(current_habit_data).T

        # Ensure columns (day labels) are sorted numerically: "1"..."31"
        day_cols = sorted(df.columns, key=lambda c: int(c))
        df = df[day_cols]

        # Initialize editor state once per month
        if (
            "habit_grid_df" not in st.session_state
            or st.session_state.data["month_key"] != current_month_key
        ):
            st.session_state.habit_grid_df = df.copy()

        # Editable grid (keep columns order stable during edit)
        edited_df = st.data_editor(
            st.session_state.habit_grid_df[day_cols],
            key="habit_grid"
        )

        # Re-apply numeric sort after edit
        edited_df = edited_df[day_cols]

        # Sync edited grid back to habit storage format (dict with string day keys)
        # Build dicts in sorted day order for deterministic column order next time
        new_data = {
            habit: {str(d): bool(edited_df.loc[habit, str(d)]) for d in day_cols}
            for habit in edited_df.index
        }
        current_habit_data.clear()
        current_habit_data.update(new_data)


# ==================================================
# JOURNAL TAB
# ==================================================

with journal:
    st.header("Daily Journal")

    # Day key within the month (DD)
    day_key = selected_date.strftime("%d")
    st.write(f"Viewing: **{current_month_key}-{day_key}**")

    # Unique key ensures text resets when date changes
    text_key = f"journal_{current_month_key}_{day_key}"

    # Load existing journal entry if present
    existing_text = current_journal_data.get(day_key, "")

    # Journal text area
    new_text = st.text_area(
        "Write your thoughts...",
        value=existing_text,
        height=300,
        key=text_key
    )

    # Update in-memory journal only (no DB write here)
    if new_text != existing_text:
        current_journal_data[day_key] = new_text


# ==================================================
# ANALYTICS TAB
# ==================================================

with graph:
    st.header("📊 Analytics & Insights")
    
    # Only show analytics if there are habits
    if not current_habit_data:
        st.info("Add some habits to see analytics!")
    else:
        with st.container(border=True, width='stretch'):
            st.plotly_chart(graphs.calculate_daily_score(current_habit_data), width='stretch')

        gcol1, gcol2 = st.columns([5,2])

        with gcol1.container(border=True):
            cols = st.columns(len(current_habit_data.keys()))

            selected_habits = []
            for col, habit in zip(cols, current_habit_data.keys()):
                with col:
                    if st.checkbox(habit, value=False):
                        selected_habits.append(habit)
            
            st.plotly_chart(graphs.plot_individual_trends(current_habit_data, selected_habits))

        with gcol2.container(border=True):
            st.plotly_chart(graphs.calculate_habit_consistency(current_habit_data))



st.markdown(
    """
    <hr>
    <div style="text-align: center; color: gray;">
        Created by <strong>Tahsin</strong> · 
        <a href="https://www.instagram.com/tahsin_2155" target="_blank">
            Instagram
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
