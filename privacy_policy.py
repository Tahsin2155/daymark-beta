import streamlit as st

st.set_page_config(page_title="Privacy Policy", layout="centered")


st.title("Privacy Policy 🔒")
st.caption("Last updated: December 2025")


st.header("What DayMark collects")
with st.container(border=True):
	st.write("DayMark collects only what is needed to run the app:")
	st.markdown(
		"- Email address (for authentication)\n"
		"- Habits and completion status\n"
		"- Journal entries\n"
		"- Tasks\n"
		"- App settings (like default reflection prompts)"
	)


st.header("How your data is used")
with st.container(border=True):
	st.write("Your data is used only to:")
	st.markdown(
		"- Authenticate your account\n"
		"- Store your habits, journal entries, tasks, and settings\n"
		"- Generate your personal analytics (based on your own data)"
	)


st.header("Data storage")
with st.container(border=True):
	st.write(
		"Data is stored using Firebase services. Your journal entries are private to your account and are not "
		"shared publicly by the app. No one can see your data except you."
	)


st.header("Data sharing")
with st.container(border=True):
	st.write("DayMark does not:")
	st.markdown(
		"- Sell your data\n"
		"- Share your data with third parties for advertising\n"
		"- Run social features that expose your content"
	)


st.header("Data deletion")
with st.container(border=True):
	st.write(
		"If you want your account or data deleted, contact the developer. "
		"(If you add an in-app deletion flow later, update this section.)"
	)


st.header("Changes to this policy")
with st.container(border=True):
	st.write(
		"This policy may be updated over time. Continued use of DayMark means you accept the latest version."
	)


st.divider()
cta1, cta2 = st.columns(2)
with cta1:
	if st.button("Back to DayMark", width="stretch"):
		st.switch_page("main.py")

with cta2:
	if st.button("Terms of Use",width="stretch"): 
		st.switch_page("terms_of_use.py")
