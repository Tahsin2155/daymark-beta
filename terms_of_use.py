"""Terms of Use for DayMark.

Legal terms governing the use of the DayMark application.

Last updated: 28 December 2025
"""

import streamlit as st


# =============================================================================
# CONSTANTS
# =============================================================================
LAST_UPDATED = "28 December 2025"
CONTACT_EMAIL = "tahsindlg@gmail.com"
CONTACT_INSTAGRAM = "https://www.instagram.com/tahsin_2155"


st.title("Terms of Use 📜")
st.caption(f"Last updated: {LAST_UPDATED}")


st.header("1) Acceptance of Terms")
with st.container(border=True):
	st.write(
		"By accessing or using DayMark, you agree to be bound by these Terms of Use. "
		"If you do not agree with any part of these terms, please do not use the application."
	)


st.header("2) Intended Use")
with st.container(border=True):
	st.write(
		"DayMark is a personal productivity and reflection tool designed for individual use. "
		"It is **not** intended to provide medical, psychological, therapeutic, or professional advice."
	)
	st.warning(
		"If you're experiencing mental health challenges, please seek help from a qualified professional."
	)


st.header("3) Service Availability")
with st.container(border=True):
	st.write(
		"We strive to keep DayMark running smoothly, but we cannot guarantee:"
	)
	st.markdown(
		"- 100% uptime or availability\n"
		"- That the service will be error-free\n"
		"- That data will never be lost"
	)
	st.info(
		"**Recommendation:** Click \"Save Changes\" after important edits to minimize data loss risk."
	)


st.header("4) User Responsibilities")
with st.container(border=True):
	st.write("As a user, you are responsible for:")
	st.markdown(
		"- Keeping your login credentials secure and confidential\n"
		"- Saving your work (click **Save Changes** after important edits)\n"
		"- Using the app in compliance with applicable laws\n"
		"- Not attempting to exploit, hack, or disrupt the service"
	)
	st.caption(
		"Note: DayMark auto-saves about every 1–1.5 minutes during active use, "
		"and logging out also saves your data."
	)


st.header("5) Service Modifications")
with st.container(border=True):
	st.write(
		"We reserve the right to modify, suspend, or discontinue DayMark at any time, "
		"with or without notice. We may also update these terms periodically."
	)


st.header("6) Limitation of Liability")
with st.container(border=True):
	st.write(
		"To the maximum extent permitted by law, the developer shall not be liable for:"
	)
	st.markdown(
		"- Any loss of data or content\n"
		"- Missed habits or personal goals\n"
		"- Any indirect, incidental, or consequential damages\n"
		"- Any outcomes resulting from the use or inability to use the app"
	)
	st.write(
		"DayMark is provided \"as is\" without warranties of any kind, either express or implied."
	)


st.header("7) Account Termination")
with st.container(border=True):
	st.write(
		"We reserve the right to terminate or suspend your account if you violate these terms "
		"or engage in behavior that harms the service or other users."
	)
	st.write(
		"You may request account deletion at any time by contacting us."
	)


st.header("8) Contact")
with st.container(border=True):
	st.write("Questions about these terms? Contact us:")
	col1, col2 = st.columns(2)
	with col1:
		st.markdown(f"📸 [Instagram]({CONTACT_INSTAGRAM}) *(fastest)*")
	with col2:
		st.markdown(f"📧 [{CONTACT_EMAIL}](mailto:{CONTACT_EMAIL})")


st.divider()
cta1, cta2 = st.columns(2)
with cta1:
	if st.button('Open DayMark', width='stretch'):
		st.switch_page("main.py")

with cta2:
	if st.button("Privacy Policy", width='stretch'):
		st.switch_page("privacy_policy.py")

st.caption(f"Last updated: {LAST_UPDATED}")
