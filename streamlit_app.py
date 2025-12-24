import streamlit as st

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
        'HIW.py',
        title='How DayMark Works',
        url_path='howitworks',
        icon=':material/help_outline:'
    ),

    st.Page(
        'privacy_policy.py',
        title='Privacy & Policy',
        url_path='pp',
        icon=':material/privacy_tip:'
    ),

    st.Page(
        'terms_of_use.py',
        title='Terms of Use',
        url_path='tou',
        icon=':material/gavel:'
    ),
]


current = st.navigation(pages, position="sidebar")
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