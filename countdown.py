import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo
import time

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="DayMark",
    layout="centered"
)

# -------------------------------
# IST timezone (server-enforced)
# -------------------------------
IST = ZoneInfo("Asia/Kolkata")

TARGET_TIME_IST = datetime(2026, 1, 1, 0, 0, 0, tzinfo=IST)
now_ist = datetime.now(IST)

# ============================================================
# BEFORE LAUNCH — apply ALL custom CSS + landing UI
# ============================================================
if now_ist < TARGET_TIME_IST:

    # ---------- Scoped CSS ----------
    # We use var(--variable-name) to reference Streamlit's native theme colors
    st.markdown("""
    <style>
        .block-container {
            padding-top: 4rem;
            padding-bottom: 4rem;
        }

        /* HEADINGS */
        h1 {
            text-align: center;
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: var(--text-color); /* Adapts to theme */
        }

        .subtitle {
            text-align: center;
            color: var(--text-color);
            opacity: 0.7; /* Slightly simpler than hardcoded gray */
            margin-bottom: 3rem;
            font-size: 1.05rem;
        }

        /* FLEX CONTAINER UPDATES */
        .countdown-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap; 
            gap: 2rem;
            margin: 0 auto;
        }

        /* BOX STYLING OPTIMIZED FOR BOTH THEMES */
        .countdown-box {
            /* Uses Streamlit's 'secondary' background (light gray in Light mode, dark gray in Dark mode) */
            background-color: var(--secondary-background-color); 
            border-radius: 18px;
            padding: 1.75rem 2rem;
            min-width: 120px;
            text-align: center;
            
            /* Universal border/shadow that looks good on both */
            border: 1px solid rgba(128, 128, 128, 0.2);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            
            flex: 1 1 150px; 
            max-width: 200px;
        }

        .countdown-number {
            font-size: 2.75rem;
            font-weight: 700;
            /* Uses the theme's Primary Color (often Red/Orange in default, or custom set) */
            color: var(--primary-color); 
            line-height: 1;
        }

        .countdown-label {
            margin-top: 0.5rem;
            font-size: 0.9rem;
            letter-spacing: 0.1em;
            color: var(--text-color);
            text-transform: uppercase;
            opacity: 0.8;
        }

        /* MOBILE RESPONSIVE TWEAKS */
        @media (max-width: 600px) {
            h1 { font-size: 2rem; }
            
            .countdown-container {
                gap: 1rem; 
            }

            .countdown-box {
                padding: 1rem;
                min-width: 130px; 
            }

            .countdown-number {
                font-size: 2rem; 
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # ---------- Countdown Logic ----------
    # Calculate initial remaining time
    remaining = TARGET_TIME_IST - now_ist
    
    # Create a placeholder to prevent UI flashing
    placeholder = st.empty()

    # We do the calculation once per rerun here
    days = remaining.days
    hours, rem = divmod(remaining.seconds, 3600)
    minutes, seconds = divmod(rem, 60)

    with placeholder.container():
        st.markdown("<h1>DayMark</h1>", unsafe_allow_html=True)
        st.markdown(
            "<div class='subtitle'>Launching in India on 1 January 2026 (IST)</div>",
            unsafe_allow_html=True
        )

        st.markdown(f"""
        <div class="countdown-container">
            <div class="countdown-box">
                <div class="countdown-number">{days}</div>
                <div class="countdown-label">Days</div>
            </div>
            <div class="countdown-box">
                <div class="countdown-number">{hours:02d}</div>
                <div class="countdown-label">Hours</div>
            </div>
            <div class="countdown-box">
                <div class="countdown-number">{minutes:02d}</div>
                <div class="countdown-label">Minutes</div>
            </div>
            <div class="countdown-box">
                <div class="countdown-number">{seconds:02d}</div>
                <div class="countdown-label">Seconds</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        if st.button('Introduction To DayMark', use_container_width=True):
            st.switch_page('intro.py')

    # Wait and Rerun
    time.sleep(1)
    st.rerun()