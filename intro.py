"""DayMark Introduction / Landing Page

This page is designed to be the first thing new users see.
It explains what DayMark is, why it exists, and how to get started.

Last updated: 28 December 2025
"""

import os
import streamlit as st



# =============================================================================
# CONSTANTS
# =============================================================================
VERSION = "1.0.1"
LAST_UPDATED = "28 December 2025"


def get_user_count() -> str:
    """Get user count from secrets, or return default text."""
    try:
        count = st.secrets.get("app", {}).get("user_count", None)
        if count:
            return f"{count}+ users building better habits"
    except Exception:
        pass
    return "Join users building better habits"


def show_optional_media() -> None:
    """Show optional hero image/video if files exist."""
    if os.path.exists("assets/daymark_hero.png"):
        st.image("assets/daymark_hero.png", caption="DayMark - Your private habit tracker")
    
    if os.path.exists("assets/daymark_intro.mp4"):
        st.subheader("Quick tour")
        st.video("assets/daymark_intro.mp4")


# =============================================================================
# Hero Section
# =============================================================================

st.title("DayMark 📓")
st.subheader("Build consistency. Reflect daily. Understand yourself.")

st.write(
    "DayMark is your private habit tracker and journaling space — designed for people who want "
    "steady progress without the pressure of streaks, public feeds, or perfection."
)

if st.button("🚀 Get Started Free", width='stretch', type="primary"):
    st.switch_page("main.py")
# Prominent CTA at top (Task 2)
# cta_col1, cta_col2 = st.columns(2)
# with cta_col1:
#     if st.button("🚀 Get Started Free", width='stretch', type="primary"):
#         st.switch_page("main.py")
# with cta_col2:
#     if st.button("📖 Learn More", width='stretch'):
#         st.write("")  # Scroll down handled by page flow

# Trust signals (Task 3)
st.markdown("---")
trust_col1, trust_col2, trust_col3 = st.columns(3)
with trust_col1:
    st.markdown(f"**👥 {get_user_count()}**")
with trust_col2:
    st.markdown("**🔒 100% Private**")
with trust_col3:
    st.markdown("**⚡ Built with Streamlit & Firebase**")

st.divider()

# show_optional_media()


# -----------------------------------------------------------------------------
# What you can do
# -----------------------------------------------------------------------------

st.header("What you can do with DayMark")

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.subheader("📊 See your progress at a glance")
        st.write(
            "Track habits in a clean monthly grid. Each habit is a row, each day is a column — "
            "so you can spot patterns instantly and know exactly where you stand."
        )
        st.markdown(
            "- Add or remove habits anytime\n"
            "- Check off completed days with one click\n"
            "- No streak anxiety — just honest visibility"
        )

    with st.container(border=True):
        st.subheader("✍️ Capture your thoughts in seconds")
        st.write(
            "Write quick daily reflections that help you understand yourself better. "
            "Set custom prompts in Settings to guide your journaling."
        )
        st.markdown(
            "- One focused entry per day\n"
            "- Optional guided prompts\n"
            "- Edit past entries anytime"
        )

with col2:
    with st.container(border=True):
        st.subheader("📈 Understand your patterns")
        st.write(
            "Simple charts show your progress without overwhelm: daily scores, "
            "consistency rankings, and habit trends over time."
        )
        st.markdown(
            "- Daily score: see your productive days\n"
            "- Consistency: find your strongest habits\n"
            "- Trends: compare habits side by side"
        )

    with st.container(border=True, height='stretch'):
        st.subheader("✅ Stay on top of daily tasks")
        st.write(
            "Keep simple to-do lists for each day. A lightweight task manager that "
            "helps you take action without getting in the way."
        )
        st.markdown(
            "- Add tasks for any day\n"
            "- Check them off as you finish\n"
            "- Track completion progress"
        )


st.divider()


# -----------------------------------------------------------------------------
# Philosophy & purpose
# -----------------------------------------------------------------------------

st.header("Philosophy")

p1, p2, p3 = st.columns(3)
with p1:
    with st.container(border=True, height='stretch'):
        st.subheader("Awareness over streaks")
        st.write(
            "Streaks can motivate — but they can also create guilt. DayMark focuses on "
            "showing your reality so you can improve calmly."
        )

with p2:
    with st.container(border=True, height='stretch'):
        st.subheader("Private by design")
        st.write(
            "No social feed. No public profile. No comparison. Your habits and journal are "
            "for you — not an audience."
        )

with p3:
    with st.container(border=True, height='stretch'):
        st.subheader("Small steps, long-term change")
        st.write(
            "When you can see your patterns, you can change them. DayMark is built to support "
            "tiny daily wins that compound over time."
        )


st.header("Purpose")
st.write(
    "DayMark helps you build a life you actually like living — by making it easier to "
    "keep promises to yourself. Over time, this can improve your:"
)
st.markdown(
    "- Consistency (you do what you said you’d do)\n"
    "- Self-awareness (you understand what works for you)\n"
    "- Confidence (progress becomes visible)\n"
    "- Focus (fewer distractions, clearer routines)"
)


st.divider()


# -----------------------------------------------------------------------------
# How it works (simple, beginner-friendly)
# -----------------------------------------------------------------------------

st.header("How it works")
with st.container(border=True):
    st.markdown(
        "**1) Create an account or log in**\n"
        "Your email/password is used only for authentication.\n\n"
        "**2) Pick a date**\n"
        "The date controls what month/day you’re viewing (habits, journal, tasks).\n\n"
        "**3) Track habits and write a journal entry**\n"
        "Check off what you completed and add a short reflection if you want.\n\n"
        "**4) Save changes**\n"
        "DayMark uses manual saving to avoid accidental writes. Click **Save Changes** before closing or refreshing."
    )


st.divider()


# -----------------------------------------------------------------------------
# Privacy promise
# -----------------------------------------------------------------------------

st.header("Privacy")
with st.container(border=True):
    st.write(
        "Your data is yours. DayMark stores only what it needs to function: your habits, journal entries, "
        "tasks, and settings. There’s no social layer and no public sharing."
    )
    st.markdown(
        "- No feed, no followers, no leaderboard\n"
        "- Your journal is private to your account\n"
        "- Analytics are computed from your own data"
    )


st.divider()


# -----------------------------------------------------------------------------
# Calls to action
# -----------------------------------------------------------------------------

st.header("Get started")

cta1, cta2 = st.columns(2)
with cta1:
    if st.button("🔐 Log in / Sign up", width='stretch'):
        st.switch_page("main.py")

with cta2:
    if st.button("About DayMark", width='stretch'):
        st.switch_page("about.py")


st.caption(
    "💡 Tip: Start with 2–3 simple habits and keep journal entries short. "
    "Consistency is easier when you begin small."
)


# =============================================================================
# FAQ Section (Task 23)
# =============================================================================
st.divider()
st.header("Frequently Asked Questions")

with st.expander("🔒 Is my data private?"):
    st.write(
        "Yes, completely. DayMark has no social features, no public profiles, and no data sharing. "
        "Your habits, journal entries, and tasks are visible only to you. We use Firebase for "
        "secure authentication and storage."
    )

with st.expander("📤 Can I export my data?"):
    st.write(
        "Data export is not yet available in the app, but we're working on it. "
        "If you need your data urgently, contact us and we'll help you get it."
    )

with st.expander("😅 What happens if I miss a day?"):
    st.write(
        "Nothing bad! DayMark doesn't punish you for missing days. There are no streaks to break, "
        "no notifications to guilt you. Just pick up where you left off. Missing a day is feedback, "
        "not failure."
    )

with st.expander("🗑️ How do I delete my account?"):
    st.write(
        "To delete your account and all associated data, contact us via Instagram (@tahsin_2155) "
        "or email (tahsindlg@gmail.com). We'll process your request promptly."
    )

with st.expander("💾 How does saving work?"):
    st.write(
        "DayMark auto-saves about every 1–1.5 minutes while you're using the app. "
        "Logging out also saves your data. However, we recommend clicking **Save Changes** "
        "after important edits to be safe."
    )

with st.expander("📱 Does DayMark work on mobile?"):
    st.write(
        "Yes! DayMark works in any modern browser on desktop, tablet, or mobile. "
        "The interface adapts to your screen size."
    )

with st.expander("📅 Why can't I select certain dates?"):
    st.write(
        "DayMark limits date selection for a reason: you can only view dates **from your account creation date up to today**. "
        "Future dates are disabled because you can't complete habits or write reflections for days that haven't happened yet. "
        "Dates before your account was created are also unavailable since there's no data to show."
    )


# =============================================================================
# Footer
# =============================================================================
st.divider()
footer1, footer2, footer3 = st.columns(3)
with footer1:
    if st.button("About", width='stretch'):
        st.switch_page("about.py")
with footer2:
    if st.button("Privacy", width='stretch'):
        st.switch_page("privacy_policy.py")
with footer3:
    if st.button("Terms", width='stretch'):
        st.switch_page("terms_of_use.py")

st.caption(f"Version {VERSION} · Last updated: {LAST_UPDATED}")

