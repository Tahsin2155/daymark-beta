import streamlit as st

st.set_page_config(page_title="How DayMark Works", layout="centered")


st.title("How DayMark Works ⚙️")
st.caption("A quick guide to the main features and how to use them well.")


st.header("1) Habits (monthly)")
with st.container(border=True):
	st.write(
		"Habits are tracked in a monthly grid. Each habit is a row, and each day is a checkbox. "
		"This makes it easy to see patterns across the month."
	)
	st.markdown(
		"- Add habits anytime\n"
		"- Delete habits you no longer need\n"
		"- Mark completion for each day"
	)


st.header("2) Journal (daily)")
with st.container(border=True):
	st.write(
		"Each date has its own journal entry. You can keep it short — even a few lines can be powerful."
	)
	st.markdown(
		"- One entry per day\n"
		"- You can set default prompts in Settings\n"
		"- You can edit older entries"
	)


st.header("3) Tasks (daily)")
with st.container(border=True):
	st.write(
		"Tasks are one-time to-dos for a specific date. Use them for practical actions that support your habits."
	)
	st.markdown(
		"- Add tasks for today or any past day\n"
		"- Check them off as you finish\n"
		"- See completion progress"
	)


st.header("4) Analytics (insights)")
with st.container(border=True):
	st.write("Analytics are computed only from your own habit data.")
	st.markdown(
		"- **Daily score:** total habits completed per day\n"
		"- **Consistency:** total completions per habit\n"
		"- **Trends:** compare selected habits over time"
	)


st.header("5) Saving")
with st.container(border=True):
	st.write(
		"DayMark auto-saves about every 1–1.5 minutes while you're using the app. "
		"Logout also saves before exiting."
	)
	st.info(
		"It's still a good idea to click **Save Changes** after important edits — just to be safe."
	)


st.header("6) Privacy")
with st.container(border=True):
	st.write(
		"DayMark is private by design: no feed, no followers, no public profile. Your account data is tied to you."
	)


st.divider()
cta1, cta2 = st.columns(2)
with cta1:
	if st.button("Open DayMark", width='stretch'):
		st.switch_page("main.py")

with cta2:
	if st.button("Privacy & Policy", width='stretch'):
		st.switch_page("privacy_policy.py")
