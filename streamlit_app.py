"""DayMark - Main Application Entry Point

This is the main Streamlit application file that sets up navigation
and runs the multi-page app.

Last updated: 28 December 2025
"""

import streamlit as st
from datetime import datetime

st.set_page_config(page_icon='assets/logo.png')



st.logo('assets/logo.png', size='large', icon_image='assets/logo.png', link='https://daymark.streamlit.app')



pages = [
    st.Page(
        'intro.py',
        title='Introduction to DayMark',
        url_path='daymark',
        icon=':material/home:'
    ),

    st.Page(
        'main.py',
        title='DayMark',
        default=True,
        icon=':material/dashboard:'
    ),

    st.Page(
        'settings.py',
        title='Settings',
        url_path='settings',
        icon=':material/settings:'
    ),

    st.Page(
        'about.py',
        title='About DayMark',
        url_path='about',
        icon=':material/info:'
    ),

    st.Page(
        'how_it_works.py',
        title='How DayMark Works',
        url_path='howitworks',
        icon=':material/help_outline:'
    ),

    st.Page(
        'privacy_policy.py',
        title='Privacy & Policy',
        url_path='privacypolicy',
        icon=':material/privacy_tip:'
    ),

    st.Page(
        'terms_of_use.py',
        title='Terms of Use',
        url_path='termsofuse',
        icon=':material/gavel:'
    ),
]

if ('user' not in st.session_state) or (st.session_state.user == None):
    del pages[2]  # Remove Settings if not logged in

current = st.navigation(pages, position="sidebar" if st.session_state.get('user') else "top")
current.run()



# footer…

st.markdown(
    """
    <hr>
    <div style="text-align: center; color: gray;">
        Created by <strong>Tahsin</strong> · 
        <a href="https://www.instagram.com/tahsin_2155" target="_blank">
            Instagram
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

