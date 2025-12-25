import streamlit as st


st.set_page_config(page_title="About DayMark", layout="centered")


st.title("About DayMark 📓")
st.caption("Why it exists, what it believes, and what it helps you do.")


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
		"That means your account is tied to your email, and your data is stored per user and per month."
	)


st.divider()
st.header("Next")

cta1, cta2 = st.columns(2)
with cta1:
	if st.button("Open DayMark", width='stretch'):
		st.switch_page("main.py")

with cta2:
	if st.button("How it works", width='stretch'):
		st.switch_page("HIW.py")
