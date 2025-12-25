"""DayMark introduction / landing page.

This page is designed to be the first thing new users see.
It explains what DayMark is, why it exists, and how to get started.

Tip: You can optionally add your own media files:
- docs/daymark_hero.png       (shown near the top)
- docs/daymark_intro.mp4      (shown in the "Quick tour" section)
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st


st.set_page_config(
    page_title="DayMark – Build Consistency, Reflect Daily",
    layout="centered"
)






def show_optional_media() -> None:
    """Show optional hero image/video if the user added them in /docs."""

    # st.image does not support width='stretch'; leaving it default keeps this compatible.
    st.image("assets/daymark_hero.png")

    # Only show the video section if a file exists.
    st.subheader("Quick tour")
    st.video("assets/daymark_intro.mp4")


# -----------------------------------------------------------------------------
# Hero
# -----------------------------------------------------------------------------

st.title(f"DayMark 📓")
st.subheader("Build consistency. Reflect daily. Understand yourself.")

st.write(
    "DayMark is a private habit tracker and journaling space built for people who want "
    "steady progress — without the pressure of streaks, public feeds, or perfection."
)

# show_optional_media()

st.divider()


# -----------------------------------------------------------------------------
# What you can do
# -----------------------------------------------------------------------------

st.header("What you can do with DayMark")

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.subheader("Habits (monthly grid)")
        st.write(
            "Track habits in a clean month view. Each habit is a row, each day is a column — "
            "so you can see patterns at a glance."
        )
        st.markdown(
            "- Add or remove habits anytime\n"
            "- Check off days you completed\n"
            "- No streak pressure — just visibility"
        )

    with st.container(border=True, height='stretch'):
        st.subheader("Journal (daily reflection)")
        st.write(
            "Write a short entry for any day. If you like prompts, you can set default "
            "reflection questions in Settings."
        )
        st.markdown(
            "- One entry per day\n"
            "- Guided prompts (optional)\n"
            "- Edit past entries anytime"
        )

with col2:
    with st.container(border=True):
        st.subheader("Analytics (insights, not judgment)")
        st.write(
            "See your progress through simple charts: daily score, consistency, and habit trends."
        )
        st.markdown(
            "- Daily score: habits completed per day\n"
            "- Consistency: which habits you keep most\n"
            "- Trends: compare selected habits"
        )

    with st.container(border=True):
        st.subheader("Tasks (daily to-dos)")
        st.write(
            "Keep simple one-off tasks for each day. It’s a lightweight to-do list that stays "
            "out of your way."
        )
        st.markdown(
            "- Add/remove tasks per day\n"
            "- Check them off as you go\n"
            "- See completion progress"
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
    "Tip: If you're new, start with 2–3 simple habits and keep journal entries short. "
    "Consistency is easier when you make the first version small."
)


# Footer links
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

