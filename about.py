"""About DayMark page.

Information about the app, its philosophy, and the creator.

Last updated: 28 December 2025
"""

import streamlit as st


# =============================================================================
# CONSTANTS
# =============================================================================
VERSION = "1.0.0"
LAST_UPDATED = "28 December 2025"

# Creator info - easy to update
CREATOR = {
    "name": "Tahsin",
    "email": "tahsindlg@gmail.com",
    "instagram": "https://www.instagram.com/tahsin_2155",
    "github": "https://github.com/Tahsin2155",  # Update with your actual GitHub URL
    # Add more links here as needed:
    # "twitter": "https://twitter.com/...",
    # "linkedin": "https://linkedin.com/in/...",
}


st.title("About DayMark 📓")
st.caption(f"Version {VERSION} · Last updated: {LAST_UPDATED}")


with st.container(border=True):
	st.subheader("The short version")
	st.write(
		"DayMark is a private habit tracker and daily journal designed to support steady improvement. "
		"It’s built for people who want clarity and consistency — not pressure."
	)


st.header("What DayMark believes")
belief1, belief2, belief3 = st.columns(3)

with belief1:
	with st.container(border=True, height="stretch"):
		st.subheader("Awareness beats intensity")
		st.write(
			"Most change starts with noticing patterns. DayMark makes patterns visible so you can adjust calmly."
		)

with belief2:
	with st.container(border=True, height="stretch"):
		st.subheader("Reflection > perfection")
		st.write(
			"A missed day isn't failure — it's feedback. DayMark is designed to help you learn, not judge."
		)

with belief3:
	with st.container(border=True, height="stretch"):
		st.subheader("Private by design")
		st.write(
			"No feed, no followers, no comparison. Your habits and journal are for you."
		)


st.header("What it helps you improve")
with st.container(border=True):
	st.markdown(
		"- **Consistency:** you follow through more often\n"
		"- **Self-awareness:** you understand what works for you\n"
		"- **Focus:** you reduce distractions and decision fatigue\n"
		"- **Confidence:** progress becomes visible and repeatable"
	)


st.header("How it’s built")
with st.container(border=True):
	st.write(
		"DayMark is built with Streamlit for the interface and Firebase for authentication and storage. "
		"Your account is tied to your email, and your data is stored securely per user and per month."
	)
	st.markdown(
		"- **Frontend:** Streamlit (Python)\n"
		"- **Authentication:** Firebase Auth\n"
		"- **Database:** Cloud Firestore\n"
		"- **Hosting:** Streamlit Cloud"
	)
	st.caption("DayMark is a proprietary application. Source code is not publicly available.")


# =============================================================================
# Creator Section (Task 5)
# =============================================================================
st.header("Created by")
with st.container(border=True):
	st.subheader(f"👋 {CREATOR['name']}")
	st.write(
		"DayMark was built to solve a personal problem: finding a simple, private way to track habits "
		"and reflect daily without the noise of social features or gamification pressure."
	)
	
	st.markdown("**Get in touch:**")
	contact_cols = st.columns(3)
	with contact_cols[0]:
		st.markdown(f"📧 [{CREATOR['email']}](mailto:{CREATOR['email']})")
	with contact_cols[1]:
		st.markdown(f"📸 [Instagram]({CREATOR['instagram']})")
	with contact_cols[2]:
		st.markdown(f"💻 [GitHub]({CREATOR['github']})")
	
	st.caption("For the fastest response, reach out via Instagram.")


st.divider()
st.header("Next")

cta1, cta2 = st.columns(2)
with cta1:
	if st.button("Open DayMark", width='stretch'):
		st.switch_page("main.py")

with cta2:
	if st.button("How it works", width='stretch'):
		st.switch_page("how_it_works.py")

st.caption(f"Version {VERSION} · Last updated: {LAST_UPDATED}")
