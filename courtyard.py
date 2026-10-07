import base64
import os
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="The Last Door - Courtyard",
    page_icon="🚪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize Session State
if "courtyard_modal_open" not in st.session_state:
    st.session_state.courtyard_modal_open = True

if "final_choice" not in st.session_state:
    st.session_state.final_choice = None


def load_base64_img(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""


img_b64 = load_base64_img("assets/outdoor.jpg")

# Styling
st.markdown(
    f"""
<style>
    header[data-testid="stHeader"] {{ display: none !important; }}
    footer {{ visibility: hidden !important; }}
    #MainMenu {{ visibility: hidden !important; }}
    
    .block-container {{
        padding: 0rem !important;
        margin: 0rem !important;
        max-width: 100% !important;
    }}
    
    .game-wrapper {{
        position: relative;
        width: 100vw;
        height: 100vh;
        background: url('data:image/jpeg;base64,{img_b64}') no-repeat center center;
        background-size: cover;
        overflow: hidden;
    }}

    .top-left-bar {{
        position: absolute;
        top: 25px;
        left: 35px;
        z-index: 10;
        color: white;
        text-shadow: 0 2px 6px rgba(0,0,0,0.8);
    }}
    .top-left-bar .title {{ font-size: 26px; font-weight: 700; }}
    .top-left-bar .subtitle {{ font-size: 13px; color: #cccccc; margin-top: 2px; }}

    .top-right-bar {{
        position: absolute;
        top: 25px;
        right: 35px;
        z-index: 10;
        display: flex;
        gap: 12px;
    }}
    .stat-badge {{
        background: rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        padding: 6px 14px;
        border-radius: 12px;
        font-size: 12px;
        color: white;
        text-align: center;
    }}
    .stat-badge .val {{ font-weight: bold; color: #48cae4; font-size: 14px; }}

    .bottom-left-tag {{
        position: absolute;
        bottom: 25px;
        left: 35px;
        z-index: 10;
        font-size: 13px;
        letter-spacing: 1px;
        color: rgba(255, 255, 255, 0.7);
        text-shadow: 0 2px 4px rgba(0,0,0,0.8);
    }}

    /* Decision Popup Messaging Card Styling */
    .msg-card {{
        background: rgba(25, 27, 31, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 12px 16px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .msg-avatar {{
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: #3a3e4a;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
    }}
    .msg-sender {{ font-size: 13px; font-weight: 600; color: #ffffff; }}
    .msg-text {{ font-size: 13px; color: #bbbbbb; margin-top: 2px; }}
    
    .review-evidence-btn {{
        text-align: center;
        margin-top: 15px;
        font-size: 13px;
        color: #888888;
        cursor: pointer;
    }}
</style>
""",
    unsafe_allow_html=True,
)


# Dialog Modal
@st.dialog("FINAL DECISION", width="large")
def show_courtyard_decision_modal():
    st.markdown("### Someone is waiting outside.")
    st.markdown(
        "<div style='color: #aaaaaa; font-size: 14px; margin-bottom: 20px;'>The key is in your hand.</div>",
        unsafe_allow_html=True,
    )

    # Message 1: Fahad
    st.markdown(
        """
        <div class="msg-card">
            <div class="msg-avatar">👤</div>
            <div>
                <div class="msg-sender">Fahad — Brother</div>
                <div class="msg-text">Turn the key. I'm right here.</div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Message 2: Unknown Number
    st.markdown(
        """
        <div class="msg-card">
            <div>
                <div class="msg-sender">Unknown number</div>
                <div class="msg-text">Stay inside. We're almost there.</div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "Unlock the gate and leave",
            type="primary",
            use_container_width=True,
            key="btn_unlock",
        ):
            st.session_state.final_choice = "unlock"
            st.success("You unlocked the gate...")
            st.rerun()

    with col2:
        if st.button(
            "Keep the gate locked and wait",
            use_container_width=True,
            key="btn_wait",
        ):
            st.session_state.final_choice = "wait"
            st.warning("You kept the gate locked...")
            st.rerun()

    st.markdown(
        "<div class='review-evidence-btn'>Review evidence</div>",
        unsafe_allow_html=True,
    )


# Trigger Pop-up
if st.session_state.courtyard_modal_open:
    show_courtyard_decision_modal()

# Main Background Canvas
st.markdown(
    """
<div class="game-wrapper">
    <div class="top-left-bar">
        <div class="title">آخر باب | THE LAST DOOR</div>
        <div class="subtitle">Chapter: Courtyard</div>
    </div>

    <div class="bottom-left-tag">FINAL DECISION</div>
</div>
""",
    unsafe_allow_html=True,
)