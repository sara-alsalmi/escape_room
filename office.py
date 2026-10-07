import streamlit as st
import time
import base64

# Page configuration
st.set_page_config(
    page_title="The Last Door - Office",
    page_icon="🚪",
    layout="wide",
    initial_sidebar_state="collapsed",
)


st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    footer { visibility: hidden !important; }
    #MainMenu { visibility: hidden !important; }
    .block-container {
        padding: 0rem !important;
        margin: 0rem !important;
        max-width: 100% !important;
    }
    
    .clue-caption {
        font-size: 13px;
        color: #555555;
        margin-top: 8px;
        margin-bottom: 12px;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# Session state initialization
if "game" not in st.session_state:
    st.session_state.game = {
        "p1_cleared": False,
        "p2_cleared": False,
        "p3_cleared": False,
    }

if "active_modal" not in st.session_state:
    st.session_state.active_modal = None

if "puzzle_hints" not in st.session_state:
    st.session_state.puzzle_hints = {
        "p1_active_level": 0,
        "p2_active_level": 0,
        "p3_active_level": 0
    }


if "clicked_pin" in st.query_params:
    st.session_state.active_modal = st.query_params["clicked_pin"]
    st.query_params.clear()
    st.rerun()


# Dialog Modals
@st.dialog("Najdi Pattern")
def open_puzzle_1_modal():
    _, col_img, _ = st.columns([1, 2, 1])
    with col_img:
        st.image("assets/Najd-pattern.png", width=300)
        
    st.markdown("<div class='clue-caption'>Inspect the traditional geometric wall motif near the door:</div>", unsafe_allow_html=True)
    st.markdown("**Puzzle 1:** What is the total sum of triangles pattern?")
    ans1 = st.text_input("Enter the number:", key="m_p1_in").strip()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Answer", type="primary", key="p1_sub", use_container_width=True):
            if ans1 == "66":
                st.session_state.game["p1_cleared"] = True
                st.session_state.puzzle_hints["p1_active_level"] = 0
                st.session_state.active_modal = None  
                st.success("Correct!")
                time.sleep(0.8)
                st.rerun()
            else:
                st.error("Incorrect answer. Try again.")

    with col2:
        if st.button("Need a Hint?", key="p1_hint_btn", use_container_width=True):
            current_level = st.session_state.puzzle_hints.get("p1_active_level", 0)
            if current_level < 3:
                st.session_state.puzzle_hints["p1_active_level"] = current_level + 1

    p1_hints_data = {
        1: "Count the number of the triangle in the image.",
        2: "Count the top and lower triangles.",
        3: "Count inner triangles."
    }
    active_level = st.session_state.puzzle_hints.get("p1_active_level", 0)
    if active_level > 0:
        st.info(f"**Hint {active_level}:** {p1_hints_data[active_level]}")


@st.dialog("Founding Day")
def open_puzzle_2_modal():
    if not st.session_state.game.get("p1_cleared", False):
        st.warning("Complete Puzzle 1 first!")
        if st.button("Close", key="p2_close", use_container_width=True):
            st.session_state.active_modal = None
            st.rerun()
        return
        
    st.markdown("<div class='clue-caption'>Inspect the official Saudi Founding Day flag standing on the desk:</div>", unsafe_allow_html=True)
    st.markdown("**Puzzle 2:** What is the Gregorian founding year written in Arabic numerals on the emblem?")
    ans2 = st.text_input("Enter 4-digit year:", key="m_p2_in").strip()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Answer", type="primary", key="p2_sub", use_container_width=True):
            if ans2 == "1727":
                st.session_state.game["p2_cleared"] = True
                st.session_state.puzzle_hints["p2_active_level"] = 0
                st.session_state.active_modal = None  # Clear modal
                st.success("Correct!")
                time.sleep(0.8)
                st.rerun()
            else:
                st.error("Incorrect year.")

    with col2:
        if st.button("Need a Hint?", key="p2_hint_btn", use_container_width=True):
            current_level = st.session_state.puzzle_hints.get("p2_active_level", 0)
            if current_level < 3:
                st.session_state.puzzle_hints["p2_active_level"] = current_level + 1

    p2_hints_data = {
        1: "Read the Arabic numerals printed in the emblem.",
        2: "The Hijri year is 1139.",
        3: "Check the image of the founding day."
    }
    active_level = st.session_state.puzzle_hints.get("p2_active_level", 0)
    if active_level > 0:
        st.info(f"**Hint {active_level}:** {p2_hints_data[active_level]}")
        if active_level == 3:
            st.image("assets/Founding_day.jpg", width=320)


@st.dialog("Wall Safe Keypad")
def open_puzzle_3_modal():
    if not st.session_state.game.get("p2_cleared", False):
        st.warning("Complete Puzzle 2 first!")
        if st.button("Close", key="p3_close", use_container_width=True):
            st.session_state.active_modal = None
            st.rerun()
        return

    st.markdown("<div class='clue-caption'>Map Cipher Logbook: Locate landmark codes across the Kingdom grid.</div>", unsafe_allow_html=True)
    st.code("""
    NEOM (Northwest)        -> Code: 9
    AlUla (West)            -> Code: 4
    Diriyah (Central)       -> Code: 1
    Al Ahsa Oasis (East)    -> Code: 7
    
    Cipher Note: Order location digits by regional coordinate: WEST to EAST.
    """, language="text")
    
    exit_pin = st.text_input("Enter 4-Digit Exit Pin:", max_chars=4, key="m_pin").strip()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Unlock Safe", type="primary", key="p3_sub", use_container_width=True):
            if exit_pin == "4917":
                st.session_state.game["p3_cleared"] = True
                st.session_state.puzzle_hints["p3_active_level"] = 0
                st.session_state.active_modal = None
                st.success("You unlocked the safe!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Incorrect PIN.")

    with col2:
        if st.button("Need a Hint?", key="p3_hint_btn", use_container_width=True):
            current_level = st.session_state.puzzle_hints.get("p3_active_level", 0)
            if current_level < 3:
                st.session_state.puzzle_hints["p3_active_level"] = current_level + 1

    p3_hints_data = {
        1: "You need the spatial layout of Saudi Arabia. Identify which city is furthest West.",
        2: "Order the locations using the given code.",
        3: "We want to start with the West and end with the East"
    }
    active_level = st.session_state.puzzle_hints.get("p3_active_level", 0)
    if active_level > 0:
        st.info(f"**Hint {active_level}:** {p3_hints_data[active_level]}")



def load_base64_img(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

img_b64 = load_base64_img("assets/office.jpg")
solved_count = sum([st.session_state.game["p1_cleared"], st.session_state.game["p2_cleared"], st.session_state.game["p3_cleared"]])


html_stage = f"""
<!DOCTYPE html>
<html>
<head>
<style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
    html, body {{ width: 100vw; height: 100vh; overflow: hidden; background: #0e0e10; }}
    
    .game-stage {{
        position: relative;
        width: 100vw;
        height: 100vh;
        background: url('data:image/jpeg;base64,{img_b64}') no-repeat center center;
        background-size: cover;
    }}

    .header-overlay {{
        position: absolute;
        top: 25px;
        left: 30px;
        z-index: 10;
        text-shadow: 0 2px 6px rgba(0,0,0,0.8);
    }}
    .header-overlay .title {{ font-size: 24px; font-weight: 700; color: #ffffff; letter-spacing: 0.5px; }}
    .header-overlay .subtitle {{ font-size: 14px; color: #d0d0d0; margin-top: 3px; }}

    .top-right-bar {{
        position: absolute;
        top: 25px;
        right: 30px;
        z-index: 10;
    }}
    .stat-card {{
        background: rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(8px);
        padding: 8px 18px;
        border-radius: 20px;
        text-align: center;
        font-size: 13px;
        color: white;
    }}
    .stat-card .val {{ font-weight: bold; font-size: 15px; color: #48cae4; margin-top: 1px; }}

    .hotspot {{
        position: absolute;
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(18, 18, 20, 0.88);
        border: 1px solid rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(8px);
        padding: 6px 14px 6px 8px;
        border-radius: 20px;
        color: #ffffff;
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
        transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
        text-decoration: none;
        z-index: 20;
    }}
    .hotspot:hover {{
        transform: scale(1.08);
        border-color: #ffffff;
        background: rgba(30, 30, 35, 0.98);
    }}
    .hotspot-num {{
        width: 22px;
        height: 22px;
        border-radius: 50%;
        background: #ffffff;
        color: #000000;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 12px;
    }}

    .pin-1 {{ top: 22%; left: 57%; }}   /* Wall next to door */
    .pin-2 {{ top: 57%; left: 24%; }}   /* On paper card under lamp */
    .pin-3 {{ top: 12%; left: 44%; }}   /* Saudi image frame on wall */
</style>
</head>
<body>

<div class="game-stage">
    <div class="header-overlay">
        <div class="title">آخر باب | THE LAST DOOR</div>
        <div class="subtitle">Level 3: Office — A House in Riyadh</div>
    </div>

    <div class="top-right-bar">
        <div class="stat-card">
            <div>Puzzles Solved</div>
            <div class="val">{solved_count} / 3</div>
        </div>
    </div>

    <a href="?clicked_pin=p1" target="_self" class="hotspot pin-1">
        <div class="hotspot-num">1</div>
        <span>Najdi Pattern</span>
    </a>

    <a href="?clicked_pin=p2" target="_self" class="hotspot pin-2">
        <div class="hotspot-num">2</div>
        <span>Founding Flag</span>
    </a>

    <a href="?clicked_pin=p3" target="_self" class="hotspot pin-3">
        <div class="hotspot-num">3</div>
        <span>Saudi Image</span>
    </a>
</div>

</body>
</html>
"""

st.components.v1.html(html_stage, height=900, scrolling=False)

# Trigger dialog modals
if st.session_state.active_modal == "p1":
    open_puzzle_1_modal()
elif st.session_state.active_modal == "p2":
    open_puzzle_2_modal()
elif st.session_state.active_modal == "p3":
    open_puzzle_3_modal()