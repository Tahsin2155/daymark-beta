import streamlit as st

st.set_page_config(
    page_title="DayMark – Build Consistency, Reflect Daily",
    layout="centered"
)

st.title("DayMark 📓")
st.subheader("Build consistency. Reflect daily. Understand yourself.")

st.markdown("""
DayMark is a private habit and journaling app designed for people who care
more about **awareness and consistency** than streaks and pressure.

No feeds.  
No social comparison.  
Just you and your days.
""")

st.divider()

st.markdown("""
### ✨ What you can do with DayMark
- Track habits in a clean monthly view
- Journal daily with guided reflection
- Visualize progress with meaningful analytics
- Keep everything private and distraction-free
""")

st.divider()

st.markdown("""
### 🔐 Private by design
Your habits and journal entries are:
- Stored securely
- Visible only to you
- Never shared or sold
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.page_link("main.py", label="🔐 Log In", use_container_width=True)

with col2:
    st.page_link("main.py", label="✨ Create Account", use_container_width=True)

st.markdown(
    """
    ---
    [About](#/About_DayMark) ·
    [How It Works](#/How_It_Works) ·
    [Privacy](#/Privacy_Policy) ·
    [Terms](#/Terms_of_Use)
    """
)
