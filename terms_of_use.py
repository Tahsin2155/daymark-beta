import streamlit as st

st.set_page_config(page_title="Terms of Use", layout="centered")


st.title("Terms of Use 📜")
st.caption("Last updated: December 2025")


st.header("1) Acceptance")
with st.container(border=True):
	st.write("By using DayMark, you agree to these terms.")


st.header("2) Intended use")
with st.container(border=True):
	st.write(
		"DayMark is a personal productivity and reflection tool. "
		"It is not medical, psychological, or therapeutic advice."
	)


st.header("3) No guarantees")
with st.container(border=True):
	st.write(
		"We do our best to keep the service working and your data safe, but:"
	)
	st.markdown(
		"- Data loss is possible (not data leak)\n"
		"- Service availability is not guaranteed"
	)
	st.write("Use DayMark at your own risk.")


st.header("4) User responsibility")
with st.container(border=True):
	st.write("You are responsible for:")
	st.markdown(
		"- Keeping your login credentials secure\n"
		"- Clicking **Save Changes** after critical changes (manual save is part of the app design)\n"
		"- Note: **Logout saves your changes before exiting**, and while you keep interacting with the app, "
		"DayMark will also auto-save about every 1–1.5 minutes. Manual saving is still recommended."
	)


st.header("5) Service changes")
with st.container(border=True):
	st.write("The service may be modified or discontinued at any time.")


st.header("6) Limitation of liability")
with st.container(border=True):
	st.write("The developer is not liable for:")
	st.markdown(
		"- Loss of data\n"
		"- Missed habits\n"
		"- Personal outcomes related to using the app"
	)


st.divider()
cta1, cta2 = st.columns(2)
with cta1:
	if st.button('Open DayMark', width="stretch"):
		st.switch_page("main.py")

with cta2:
    if st.button("Privacy Policy",width="stretch"):
        st.switch_page("privacy_policy.py")
