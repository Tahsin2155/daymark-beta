"""How DayMark Works page.

A guide to the main features and how to use them effectively.

Last updated: 28 December 2025
"""

import streamlit as st


# =============================================================================
# CONSTANTS
# =============================================================================
LAST_UPDATED = "28 December 2025"


st.title("How DayMark Works ⚙️")
st.caption(f"A quick guide to the main features · Last updated: {LAST_UPDATED}")


st.header("1) 📊 Habits (Monthly Grid)")
with st.container(border=True):
	st.write(
		"Track your habits in a visual monthly grid. Each habit is a row, and each day is a checkbox. "
		"This makes it easy to spot patterns and see your consistency at a glance."
	)
	st.markdown(
		"- ➕ Add new habits anytime\n"
		"- 🗑️ Delete habits you no longer need\n"
		"- ✅ Mark completion for each day"
	)
	st.info("💡 **Tip:** Start with 2-3 habits. It's easier to build consistency when you begin small.")


st.header("2) ✍️ Journal (Daily Reflections)")
with st.container(border=True):
	st.write(
		"Each date has its own journal entry. Keep it short — even a few lines can help you "
		"understand yourself better over time."
	)
	st.markdown(
		"- 📝 One entry per day\n"
		"- 💬 Set default prompts in Settings\n"
		"- ✏️ Edit past entries anytime"
	)
	st.info("💡 **Tip:** Set reflection prompts in Settings to guide your journaling.")


st.header("3) ✅ Tasks (Daily To-Dos)")
with st.container(border=True):
	st.write(
		"Tasks are one-time to-dos for a specific date. Use them for practical actions that support your habits "
		"or daily goals."
	)
	st.markdown(
		"- 📋 Add tasks for today or any past day\n"
		"- ☑️ Check them off as you finish\n"
		"- 📊 See completion progress"
	)


st.header("4) 📈 Analytics (Insights)")
with st.container(border=True):
	st.write("Understand your patterns with simple, visual analytics computed from your own data:")
	st.markdown(
		"- **Daily score:** See how many habits you completed each day\n"
		"- **Consistency:** Discover which habits you maintain best\n"
		"- **Trends:** Compare selected habits over time"
	)
	st.info("💡 **Tip:** Check Analytics weekly to spot patterns and adjust your habits.")


st.header("5) 💾 Saving Your Work")
with st.container(border=True):
	st.write(
		"DayMark uses a combination of auto-save and manual save to protect your data:"
	)
	st.markdown(
		"- **Auto-save:** Every 1–1.5 minutes while you're using the app\n"
		"- **Logout save:** Your data is saved when you log out\n"
		"- **Manual save:** Click **Save Changes** after important edits"
	)
	st.warning(
		"⚠️ Always click **Save Changes** after important edits to ensure your data is saved."
	)


st.header("6) 🔒 Privacy")
with st.container(border=True):
	st.write(
		"DayMark is private by design. Your data belongs to you and only you."
	)
	st.markdown(
		"- 🚫 No social feed or followers\n"
		"- 🚫 No public profile\n"
		"- 🚫 No data sharing\n"
		"- ✅ Your account data is tied only to you"
	)


st.divider()
cta1, cta2 = st.columns(2)
with cta1:
	if st.button("Open DayMark", width='stretch'):
		st.switch_page("main.py")

with cta2:
	if st.button("Privacy Policy", width='stretch'):
		st.switch_page("privacy_policy.py")

st.caption(f"Last updated: {LAST_UPDATED}")
