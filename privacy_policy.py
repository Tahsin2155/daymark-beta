"""Privacy Policy for DayMark.

This page outlines how we collect, use, and protect user data.

Last updated: 28 December 2025
"""

import streamlit as st


# =============================================================================
# CONSTANTS
# =============================================================================
LAST_UPDATED = "28 December 2025"
CONTACT_EMAIL = "tahsindlg@gmail.com"
CONTACT_INSTAGRAM = "https://www.instagram.com/tahsin_2155"


st.title("Privacy Policy 🔒")
st.caption(f"Last updated: {LAST_UPDATED}")


st.header("What we collect")
with st.container(border=True):
	st.write("We collect only what's needed to run the app:")
	st.markdown(
		"- **Email address** — for authentication\n"
		"- **Habits and completion status** — to track your progress\n"
		"- **Journal entries** — your daily reflections\n"
		"- **Tasks** — your to-do items\n"
		"- **App settings** — like default reflection prompts"
	)


st.header("How we use your data")
with st.container(border=True):
	st.write("We use your data only to:")
	st.markdown(
		"- Authenticate your account\n"
		"- Store your habits, journal entries, tasks, and settings\n"
		"- Generate your personal analytics (based on your own data)"
	)
	st.info("We never use your data for advertising, profiling, or selling to third parties.")


st.header("Data storage & security")
with st.container(border=True):
	st.write(
		"Your data is stored securely using Firebase services (Google Cloud infrastructure). "
		"Your journal entries are private to your account and are never shared publicly."
	)
	st.markdown(
		"**Third-party services we use:**\n"
		"- **Firebase Authentication** — secure login\n"
		"- **Cloud Firestore** — encrypted database storage\n"
		"- **Streamlit Cloud** — app hosting"
	)
	st.caption("All services comply with industry-standard security practices.")


st.header("Data sharing")
with st.container(border=True):
	st.write("**We do not:**")
	st.markdown(
		"- ❌ Sell your data\n"
		"- ❌ Share your data with advertisers\n"
		"- ❌ Use your data for profiling\n"
		"- ❌ Expose your content through social features"
	)


st.header("Your rights")
with st.container(border=True):
	st.write("You have the right to:")
	st.markdown(
		"- **Access** — request a copy of your data\n"
		"- **Rectification** — correct inaccurate data\n"
		"- **Erasure** — request deletion of your account and data\n"
		"- **Portability** — receive your data in a portable format"
	)
	st.write(
		f"To exercise these rights, contact us via "
		f"[Instagram]({CONTACT_INSTAGRAM}) (fastest) or email at {CONTACT_EMAIL}."
	)


st.header("Data retention")
with st.container(border=True):
	st.write(
		"We retain your data for as long as your account is active. "
		"If you request account deletion, we will permanently remove all your data within 30 days."
	)


st.header("Data deletion")
with st.container(border=True):
	st.write(
		"To delete your account and all associated data, contact us via:"
	)
	col1, col2 = st.columns(2)
	with col1:
		st.markdown(f"📸 [Instagram]({CONTACT_INSTAGRAM}) *(fastest)*")
	with col2:
		st.markdown(f"📧 [{CONTACT_EMAIL}](mailto:{CONTACT_EMAIL})")
	st.caption("We will process deletion requests within 30 days.")


st.header("Changes to this policy")
with st.container(border=True):
	st.write(
		"We may update this policy from time to time. When we make significant changes, "
		"we'll update the \"Last updated\" date at the top of this page. "
		"Continued use of DayMark after changes means you accept the updated policy."
	)


st.header("Contact us")
with st.container(border=True):
	st.write("Questions about this privacy policy? Reach out:")
	col1, col2 = st.columns(2)
	with col1:
		st.markdown(f"📸 [Instagram]({CONTACT_INSTAGRAM}) *(fastest)*")
	with col2:
		st.markdown(f"📧 [{CONTACT_EMAIL}](mailto:{CONTACT_EMAIL})")


st.divider()
cta1, cta2 = st.columns(2)
with cta1:
	if st.button("Back to DayMark", width='stretch'):
		st.switch_page("main.py")

with cta2:
	if st.button("Terms of Use", width='stretch'): 
		st.switch_page("terms_of_use.py")

st.caption(f"Last updated: {LAST_UPDATED}")
