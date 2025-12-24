import streamlit as st

st.set_page_config(page_title="How DayMark Works", layout="centered")

st.title("How DayMark Works ⚙️")

st.markdown("""
### 1️⃣ Habits
- Habits are tracked **monthly**
- Each habit has a checkbox for every day
- You can add or delete habits anytime
- Progress is saved per month

### 2️⃣ Journal
- Each day has its own journal entry
- You can pre-fill entries with reflection prompts
- Past entries can be edited anytime

### 3️⃣ Saving Data
⚠️ **Important:**  
DayMark uses manual saving to prevent accidental writes.

👉 Always click **“Save Changes”** before:
- Refreshing the page
- Closing the browser
- Logging out

### 4️⃣ Analytics
- **Daily Score** shows how many habits you completed per day
- **Habit Trends** show consistency over time
- **Consistency Chart** highlights long-term discipline

Analytics are calculated only from your own data.

### 5️⃣ Privacy
Everything you see is tied only to your account.
No social features. No comparisons. No tracking.
""")
