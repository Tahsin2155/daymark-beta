import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import time


# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="DayMark",
    layout="centered"
)


# -------------------------------
# IST timezone (server-enforced)
# -------------------------------
IST = ZoneInfo(st.context.timezone)

TARGET_TIME_IST = datetime(2025, 1, 1, 0, 0, 0, tzinfo=IST)
now_ist = datetime.now(IST)


# ============================================================
# BEFORE LAUNCH — apply ALL custom CSS + landing UI
# ============================================================
if now_ist < TARGET_TIME_IST:

    # ---------- Scoped CSS ----------
    st.markdown("""
    <style>
        .block-container {
            padding-top: 4rem;
            padding-bottom: 4rem;
        }

        /* HEADINGS */
        h1 {
            text-align: center;
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .subtitle {
            text-align: center;
            opacity: 0.7;
            margin-bottom: 3rem;
            font-size: 1.05rem;
        }

        /* FLEX CONTAINER UPDATES */
        .countdown-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap; 
            gap: 2rem;
            margin: 0 auto;
        }

        /* BOX STYLING */
        .countdown-box {
            border-radius: 18px;
            padding: 1.75rem 2rem;
            min-width: 120px;
            text-align: center;
            
            /* Subtle border for definition in both themes */
            border: 1px solid rgba(128, 128, 128, 0.2);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            
            flex: 1 1 150px; 
            max-width: 200px;
        }

        /* NUMBERS: UPDATED TO MATCH THEME TEXT */
        .countdown-number {
            font-size: 2.75rem;
            font-weight: 700;
            line-height: 1;
        }

        .countdown-label {
            margin-top: 0.5rem;
            font-size: 0.9rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            opacity: 0.6;
        }

        /* MOBILE RESPONSIVE TWEAKS */
        @media (max-width: 600px) {
            h1 { font-size: 2rem; }
            .countdown-container { gap: 1rem; }
            .countdown-box { padding: 1rem; min-width: 130px; }
            .countdown-number { font-size: 2rem; }
        }
    </style>
    """, unsafe_allow_html=True)

    # ---------- Countdown Logic ----------
    remaining = TARGET_TIME_IST - now_ist
    placeholder = st.empty()

    days = remaining.days
    hours, rem = divmod(remaining.seconds, 3600)
    minutes, seconds = divmod(rem, 60)

    with placeholder.container():
        st.markdown("<h1>DayMark</h1>", unsafe_allow_html=True)
        st.markdown(
            "<div class='subtitle'>Launching on 1 January 2026</div>",
            unsafe_allow_html=True
        )

        st.markdown(f"""
        <div class="countdown-container">
            <div class="countdown-box">
                <div class="countdown-number">{days}</div>
                <div class="countdown-label">Days</div>
            </div>
            <div class="countdown-box">
                <div class="countdown-number">{hours:02d}</div>
                <div class="countdown-label">Hours</div>
            </div>
            <div class="countdown-box">
                <div class="countdown-number">{minutes:02d}</div>
                <div class="countdown-label">Minutes</div>
            </div>
            <div class="countdown-box">
                <div class="countdown-number">{seconds:02d}</div>
                <div class="countdown-label">Seconds</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        if st.button('Introduction To DayMark', width='stretch', type='primary', key='intro_button'):
            st.switch_page('intro.py')

    time.sleep(1)
    st.rerun()



# ============================================================================
# DAYMARK - Habit Tracker & Journal App
# ============================================================================
# This is the main file that runs the DayMark application.
# 
# WHAT THIS APP DOES:
# - Lets users track daily habits (like "Exercise", "Read", etc.)
# - Provides a daily journal for reflection
# - Shows analytics/graphs of habit completion
# - Manages daily tasks with checkboxes
#
# HOW THE CODE IS ORGANIZED:
# - utils/auth.py   → Handles user login and signup with Firebase
# - utils/db.py     → Reads and writes data to Firestore database
# - utils/graphs.py → Creates the charts and visualizations
#
# STREAMLIT BASICS:
# - st.session_state → A dictionary that persists data between page reruns
# - st.rerun()       → Refreshes the page to show updated data
# - Widgets (buttons, inputs) automatically trigger reruns when interacted with
# ============================================================================

import streamlit as st
import datetime, copy, time
import pandas as pd
from zoneinfo import ZoneInfo
from utils import db, graphs
from utils.auth import show_auth_page

# App timezone
IST = ZoneInfo(st.context.timezone)


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
# This MUST be the first Streamlit command in the app.
# It sets the browser tab title, icon, and layout style.
st.set_page_config(
    page_title="DayMark",
    layout="wide"
)


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
# Session state is like a "memory" that survives page refreshes.
# We use it to remember:
#   - user: The logged-in user's info (or None if not logged in)
#   - settings: User preferences like name, email, reflection prompts
#   - data: The habits, journal entries, and tasks for the current month

# Check if 'user' exists in session state. If not, set it to None (not logged in)
if "user" not in st.session_state:
    st.session_state.user = None


# ============================================================================
# AUTHENTICATION (LOGIN / SIGNUP)
# ============================================================================
# If the user hasn't logged in yet, we show the login/signup form.
# Once they log in successfully, we store their info in session_state.user
# and the app continues to the main dashboard.
#
# Using show_auth_page_legacy() from new_signup.py
# To enable email verification, replace with: show_auth_page()

if not st.session_state.user:
    show_auth_page()


# ============================================================================
# MAIN APP - DATA INITIALIZATION
# ============================================================================
# If we reach here, the user is logged in!
# Now we set up the data structures to hold their habits, journal, and tasks.

# Initialize the data storage if it doesn't exist yet
# This runs only once when the user first logs in
if "data" not in st.session_state:
    st.session_state.data = {
        # habits: Dictionary where keys are habit names, values are dicts of day->boolean
        # Example: {"Exercise": {"1": True, "2": False, "3": True, ...}}
        "habits": {},
        
        # journal: Dictionary where keys are day numbers, values are the journal text
        # Example: {"1": "Today was great!", "2": "Feeling tired..."}
        "journal": {},
        
        # tasks: Dictionary where keys are day numbers, values are dicts of task->boolean
        # Example: {"1": {"Buy groceries": True, "Call mom": False}}
        "tasks": {},
        
        # month_key: Tracks which month we're currently viewing (format: "YYYY-MM")
        "month_key": None
    }

st.title("DayMark")


# ============================================================================
# DATE SELECTION & HEADER BUTTONS
# ============================================================================
# The top of the page has:
# - A date picker to select which day to view
# - A "Save Changes" button to save data to the database
# - A "Logout" button to sign out

# Create 3 columns for the header layout (5:2:2 ratio)
hcol1, hcol2, hcol3 = st.columns([5, 2, 2])

# Date picker - user can select any date from account creation to today
# This determines which month's data we load and which day's journal we show
selected_date = hcol1.date_input(
    "Select Date",
    "today",
    max_value=datetime.datetime.now(tz=IST),  # Can't select future dates
    min_value=st.session_state.settings['date_of_account_creation'],
    label_visibility='collapsed',  # Hide the label for cleaner look
)

# Extract the month ("YYYY-MM") and day ("DD") from the selected date
# month_key groups all data by month, day_key is for journal/tasks
current_month_key = selected_date.strftime("%Y-%m")  # e.g., "2025-12"
day_key = selected_date.strftime("%d")               # e.g., "21"

# Get the user's unique ID from Firebase (used for database paths)
user_id = st.session_state.user['localId']

if "savedchanges" not in st.session_state:
    st.session_state.savedchanges = copy.deepcopy(st.session_state.data)

if "last_autosave" not in st.session_state:
    # Initialize so the first autosave doesn't happen immediately.
    st.session_state.last_autosave = time.time()

# ----------------------------------------
# Save Function
# ----------------------------------------
# This function saves all current data (habits, journal, tasks) to the database
def save(data=None):
    """Save all current month's data to Firestore database."""
    if data is None:
        data = st.session_state.data

    if data != st.session_state.savedchanges:
        db.save_month_data(
            user_id,
            current_month_key,
            data["habits"],
            data["journal"],
            data["tasks"]
        )
        st.session_state.savedchanges = copy.deepcopy(st.session_state.data)
        st.session_state.last_autosave = time.time()


# ----------------------------------------
# Logout Function
# ----------------------------------------
# This function saves data and clears the session to log the user out
def logout():
    """Save data and clear session state to log user out."""
    # Try to save current data before logging out (wrapped in try/except for safety)
    try:
        if st.session_state.get("data"):
            save(st.session_state.data)
    except Exception:
        pass  # Ignore errors during logout - user is leaving anyway
    
    # Clear all session data to "forget" the user
    st.session_state.pop("habit_grid_df", None)
    st.session_state.pop("__logout_requested__", None)
    for key in ("user", "settings", "data"):
        st.session_state.pop(key, None)


# Add the buttons to the header columns
# on_click runs the function when button is pressed
hcol2.button("Save Changes", width='stretch',type='primary', on_click=save, args=(st.session_state.data,))
hcol3.button('Logout', on_click=logout, width='stretch')

if "last_autosave" in st.session_state:
    # Convert timestamp to IST for display
    last_save_ist = datetime.datetime.fromtimestamp(
        st.session_state.last_autosave, tz=IST
    )
    st.caption(f"Last saved at {last_save_ist.strftime('%H:%M:%S')}")


# Show a reminder to save before leaving
st.info(
'**Auto-save**: DayMark saves automatically every 1–1.5 minutes and when you log out.\n\n'
'Still, click Save Changes after important edits.'    
# 'Privacy: only you can see your habits, journal entries, and tasks.'
)


# ============================================================================
# MONTH CHANGE HANDLING
# ============================================================================
# When the user picks a different month, we need to:
# 1. Save the current month's data to the database
# 2. Load the new month's data from the database
# This ensures data isn't lost when switching months.

# Check if the selected month is different from what we have loaded
if current_month_key != st.session_state.data["month_key"]:

    # If we had data from a previous month, save it first (only if changed)
    if st.session_state.data['month_key']:
        # Only save if data has actually changed (dirty-check)
        if st.session_state.data != st.session_state.get('savedchanges'):
            db.save_month_data(
                user_id,
                st.session_state.data['month_key'],  # The OLD month
                st.session_state.data["habits"],
                st.session_state.data["journal"],
                st.session_state.data["tasks"]
            )

    # Now load data for the NEW month from the database
    habits, journals, tasks = db.load_month_data(user_id, current_month_key)

    # Store the loaded data in session state
    st.session_state.data["habits"] = habits
    st.session_state.data["journal"] = journals
    st.session_state.data["tasks"] = tasks
    st.session_state.data["month_key"] = current_month_key  # Remember which month we loaded

    st.session_state.savedchanges = copy.deepcopy(st.session_state.data)

    # Refresh the page so all widgets show the new data
    st.rerun()


# ============================================================================
# CONVENIENT SHORTCUTS TO DATA
# ============================================================================
# Create short variable names that point to our data.
# This makes the code cleaner and easier to read.
# (They reference the same data - changes to these affect session_state too)

current_habit_data = st.session_state.data["habits"]    # All habits for this month
current_journal_data = st.session_state.data["journal"]  # All journal entries for this month
current_task_data = st.session_state.data["tasks"]       # All tasks for this month


# ============================================================================
# MAIN TABS
# ============================================================================
# The main interface has 4 tabs:
# - Habits: Track daily habits in a grid
# - Analytics: View charts of your progress
# - Journal: Write daily reflections
# - Tasks: Manage to-do items for each day

habit, graph, journal, tasks = st.tabs(["Habits", "Analytics", "Journal", "Tasks"])


# ============================================================================
# HABIT TRACKER TAB
# ============================================================================
# This tab shows a grid where:
# - Rows = habit names (e.g., "Exercise", "Read")
# - Columns = days of the month (1, 2, 3, ... 31)
# - Cells = checkboxes (True = done, False = not done)

with habit:
    st.header("Habits")
    st.write(f"Viewing: **{current_month_key}**")  # Show which month we're looking at

    # ----------------------------------------
    # Add/Delete Habit Buttons
    # ----------------------------------------
    # The "Manage Habits" popover contains options to add or delete habits
    
    with st.popover("Manage Habits"):
        add, delete = st.tabs(["Add Habit", "Delete Habit"])

        # --- ADD A NEW HABIT ---
        with add:
            with st.form("add_habit_form"):
                new_habit_name = st.text_input("Enter New Habits Name", placeholder="Habit Name")

                if st.form_submit_button("Add Habit"):
                    if new_habit_name:  # Make sure they entered a name
                        # Create the new habit with False for every day of the month
                        # pd.Period gives us how many days are in the current month
                        days_in_month = pd.Period(current_month_key).days_in_month
                        current_habit_data[new_habit_name] = {
                            str(d): False for d in range(1, days_in_month + 1)
                        }  # Creates: {"1": False, "2": False, ...}
                        
                        # Delete the cached grid so it rebuilds with the new habit
                        if "habit_grid_df" in st.session_state:
                            del st.session_state.habit_grid_df
                        
                        st.success(f'Added {new_habit_name}')
                        st.rerun()  # Refresh to show the new habit
                    else:
                        st.error("Please enter a habit name.")

        # --- DELETE AN EXISTING HABIT ---
        with delete:
            # Dropdown menu showing all current habits
            habit_to_delete = st.selectbox(
                "Select Habit to Delete",
                current_habit_data.keys()
            )

            # Button is disabled if there's nothing to delete
            if st.button("Delete Habit", disabled=bool(not habit_to_delete)):
                del current_habit_data[habit_to_delete]  # Remove from data
                
                # Delete the cached grid so it rebuilds without this habit
                if "habit_grid_df" in st.session_state:
                    del st.session_state.habit_grid_df
                
                st.rerun()  # Refresh to update the display  # Refresh to update the display

    # ----------------------------------------
    # Habit Grid (Editable Table)
    # ----------------------------------------
    # We display habits in an editable table using st.data_editor
    # Users can click cells to toggle habits on/off

    # Show a message if the user hasn't added any habits yet
    if not current_habit_data:
        st.info("No habits found for this month. Please add some.")

    else:
        # Convert the habits dictionary to a pandas DataFrame for display
        # .T transposes it so habits are rows and days are columns
        df = pd.DataFrame(current_habit_data).T

        # Sort columns numerically ("1", "2", "3" ... not "1", "10", "11")
        day_cols = sorted(df.columns, key=lambda c: int(c))
        df = df[day_cols]

        # Store the DataFrame in session_state so edits persist between reruns
        # Only create it if it doesn't exist or if we switched months
        if (
            "habit_grid_df" not in st.session_state
            or st.session_state.data["month_key"] != current_month_key
        ):
            st.session_state.habit_grid_df = df.copy()

        # Display the editable grid - users can click cells to toggle True/False
        edited_df = st.data_editor(
            st.session_state.habit_grid_df[day_cols],
            key="habit_grid"
        )

        # Make sure columns stay sorted after editing
        edited_df = edited_df[day_cols]

        # Convert the edited DataFrame back to our dictionary format
        # This syncs the UI changes to our data structure
        new_data = {
            habit: {str(d): bool(edited_df.loc[habit, str(d)]) for d in day_cols}
            for habit in edited_df.index
        }
        # Update the habit data with the new values
        current_habit_data.clear()
        current_habit_data.update(new_data)


# ============================================================================
# JOURNAL TAB
# ============================================================================
# The journal tab lets users write daily reflections.
# Each day has its own journal entry that gets saved separately.

with journal:
    st.header("Daily Journal")

    # Show which specific day we're journaling for (e.g., "2025-12-21")
    st.write(f"Viewing: **{current_month_key}-{day_key}**")

    # Calculate and show how many habits were completed today
    # This gives users context about their day while journaling
    done = sum(
        current_habit_data[h].get(day_key, False)  # Count True values
        for h in current_habit_data
    )
    total = len(current_habit_data)  # Total number of habits

    st.markdown(f"**Habits completed:** {done} / {total}")
    st.progress(done / total if total > 0 else 0)  # Visual progress bar

    # Create a unique key for the text area based on the date
    # This ensures the widget resets properly when the date changes
    text_key = f"journal_{current_month_key}_{day_key}"

    # Load the existing journal entry for this day
    # If there's no entry yet, use the default reflection questions from settings
    existing_text = (
        current_journal_data.get(day_key, "") 
        if current_journal_data.get(day_key, "") != "" 
        else st.session_state.settings['reflection_questions']
    )

    # The journal text area - a large input box for writing
    new_text = st.text_area(
        "Write your thoughts...",
        value=existing_text,
        height=400,
        key=text_key
    )

    # If the text changed, save it to our data (in memory only)
    # The database save happens when the user clicks "Save Changes"
    if new_text != existing_text:
        current_journal_data[day_key] = new_text


# ============================================================================
# TASKS TAB
# ============================================================================
# Unlike habits (which repeat daily), tasks are one-time to-do items.
# Each day can have its own set of tasks.
# Tasks are stored as: {"21": {"Buy groceries": True, "Call mom": False}}

with tasks:
    # Split into two columns: task list on left, progress on right
    tsk, progress = st.columns(2)

    # --- TASK LIST ---
    with tsk.container(border=True):
        st.header("Tasks Management")
        st.write("Manage your tasks for the selected day.")

        # Get today's tasks (empty dict if none exist)
        task_today = current_task_data.get(day_key, {})
        
        # Add/Remove task buttons in a popover
        with st.popover("Manage Tasks"):
            add_task, remove_task = st.tabs(["Add Task", "Remove Task"])
            
            # --- ADD NEW TASK ---
            with add_task:
                with st.form("add_task_form"):
                    new_task_name = st.text_input("Enter New Task Name", placeholder="Task Name")
                    
                    if st.form_submit_button("Add Task"):
                        if new_task_name:
                            task_today[new_task_name] = False  # New tasks start unchecked
                            current_task_data[day_key] = task_today  # Save to data
                            st.success(f'Added task: {new_task_name}')
                            st.rerun()
                        else:
                            st.error("Please enter a task name.")
            
            # --- REMOVE TASK ---
            with remove_task:
                task_to_remove = st.selectbox(
                    "Select Task to Remove",
                    task_today.keys()
                )
                
                if st.button("Remove Task", disabled=bool(not task_to_remove)):
                    if task_to_remove in task_today:
                        del task_today[task_to_remove]
                        current_task_data[day_key] = task_today
                        st.success(f'Removed task: {task_to_remove}')
                        st.rerun()

        # Display each task as a checkbox
        for task, completed in task_today.items():
            task_today[task] = st.checkbox(
                task,
                value=completed,
                key=f"{day_key}_{task}"  # Unique key per day per task
            )
        
    # --- PROGRESS DISPLAY ---
    with progress.container(border=True, height='stretch'):
        st.header("Task Completion Progress")
        st.write("Track your task completion progress for the day.")
        
        # Count how many tasks are done
        value = sum(1 for v in current_task_data.get(day_key, {}).values() if v)
        total = len(current_task_data.get(day_key, {}))
        
        # Show a progress bar
        st.progress(
            value / total if total > 0 else 0, 
            text=f"{value} out of {total} tasks completed"
        )



# ============================================================================
# ANALYTICS TAB
# ============================================================================
# This tab displays visualizations of habit data:
# 1. Daily Score Chart - How many habits completed each day (line graph)
# 2. Individual Trends - Track specific habits over time
# 3. Habit Consistency - Which habits are you best at? (bar chart)

with graph:
    st.header("📊 Analytics & Insights")
    
    # Can't show charts if there's no data
    if not current_habit_data:
        st.info("Add some habits to see analytics!")
    else:
        # --- DAILY SCORE CHART ---
        # Shows a line graph of total habits completed per day
        with st.container(border=True):
            st.plotly_chart(graphs.calculate_daily_score(current_habit_data), width='stretch')

        # Two columns: left for trends, right for consistency
        gcol1, gcol2 = st.columns([5, 2])

        # --- INDIVIDUAL HABIT TRENDS ---
        # Users can select which habits to compare on the chart
        with gcol1.container(border=True):
            # Create a checkbox for each habit
            cols = st.columns(len(current_habit_data.keys()))
            selected_habits = []
            for col, habit in zip(cols, current_habit_data.keys()):
                with col:
                    if st.checkbox(habit, value=False):
                        selected_habits.append(habit)
            
            # Show the trend chart for selected habits
            st.plotly_chart(graphs.plot_individual_trends(current_habit_data, selected_habits), width='stretch')

        # --- HABIT CONSISTENCY CHART ---
        # Bar chart showing which habits have the most completions
        with gcol2.container(border=True, height='stretch'):
            st.plotly_chart(graphs.calculate_habit_consistency(current_habit_data), width='stretch')


# ============================================================================
# INTERACTION-BASED AUTOSAVE
# ============================================================================
# Streamlit reruns this script whenever the user interacts with the app.
# So “continuous interaction” naturally produces reruns.
#
# We autosave on those reruns (not via forced refresh) roughly every 1–1.5 minutes.
# This avoids constant writes while still protecting users from accidental loss.

now = time.time()
if (now - st.session_state.last_autosave) >= 60:
    try:
        save(st.session_state.data)
    except Exception:
        # Autosave should never block the UI.
        pass
