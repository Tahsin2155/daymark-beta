import streamlit as st
from utils import db

st.set_page_config(page_title="Settings", layout="centered")


st.title('Settings')
st.caption("Personalize DayMark (and set optional journal prompts).")


# Make sure expected keys exist to avoid KeyError if an older profile is missing fields.
st.session_state.settings.setdefault('name', '')
st.session_state.settings.setdefault('reflection_questions', '')


with st.container(border=True):
    st.subheader("Account")
    st.write(f"Email: **{st.session_state.settings['email']}**")
    st.write(f"Date of Account Creation: **{st.session_state.settings['date_of_account_creation']}**")


with st.container(border=True):
    st.subheader("Preferences")
    st.write(
        "You can set a default journal prompt here. DayMark will use it when a day has no journal entry yet."
    )

    with st.form('settings_form'):
        st.session_state.settings['name'] = st.text_input(
            'Name (optional)',
            value=st.session_state.settings['name'],
            placeholder='Your Name'
        )

        st.session_state.settings['reflection_questions'] = st.text_area(
            'Default journal prompt (optional)',
            value=st.session_state.settings['reflection_questions'],
            placeholder='Example:\n- What went well today?\n- What felt hard?\n- What is one small win?\n- What do I want to do tomorrow?',
            height=250
        )

        saved = st.form_submit_button('Save Changes', width='stretch')
        if saved:
            db.update_user_settings(st.session_state.user['localId'], st.session_state.settings)
            st.success("Settings saved.")


st.divider()
if st.button("Back to DayMark", width='stretch'):
    st.switch_page("main.py")