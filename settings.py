import streamlit as st
from utils import db


if ('user' not in st.session_state) or (st.session_state.user == None):
    st.switch_page('main.py')

st.title('Settings')

st.write(f"""
Email: **{st.session_state.settings['email']}**\n
Date of Account Creation: **{st.session_state.settings['date_of_account_creation']}**
""")


with st.form('settings_form'):
    st.session_state.settings['name'] = st.text_input('Enter your name', value=st.session_state.settings['name'], placeholder='Your Name')
    st.empty()
    st.session_state.settings['reflection_questions'] = st.text_area('Edit / Add default text to your Journal', value=st.session_state.settings['reflection_questions'], placeholder='Reflection', height=250)

    if st.form_submit_button('Save Changes'):
        db.update_user_settings(st.session_state.user['localId'], st.session_state.settings)