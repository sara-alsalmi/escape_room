import base64
import os
import time
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="The Last Door - Office",
    page_icon="🚪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
if "current_screen" not in st.session_state:
    st.session_state.current_screen = "office"

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
        "p3_active_level": 0,
    }


# -----------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------
def load_base64_img(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""


def safe_image(image_path, **kwargs):
    if os.path.exists(image_path):
        st.image(image_path, **kwargs)
    else:
        st.warning(f"Image missing: {image_path}")


# -----------------------------------------------------------------------------
# DIALOG MODALS
# -----------------------------------------------------------------------------
@st.dialog("EVIDENCE", width="large")
def show_evidence_modal():
    st.markdown(
        "<div class='ev-header-title'>The contact name is not proof.</div>",
        unsafe_allow_html=True,
    )

    _, col_img, _ = st.columns([0.5, 3, 0.5])
    with col_img:
        safe_image("assets/open_door.jpg", use_container_width=True)

    st.markdown(
        "<div class='ev-subtext'>The blue case matches Fahad's phone.</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class='ev-box'>
            <div style='color: #888; font-size: 11px; margin-bottom: 4px;'>Saved message</div>
            <i>"I've secured the stairwell door. Someone is at the gate. I'm going to get help."</i>
        </div>
    """,
        unsafe_allow_html=True,
    )

    btn_col1, btn_col2 = st.columns([2, 2])
    with btn_col1:
        if st.button(
            "Continue to courtyard",
            type="primary",
            use_container_width=True,
            key="next_courtyard_btn",
        ):
            st.session_state.active_modal = None
            st.session_state.current_screen = "courtyard"
            st.rerun()
    with btn_col2:
        if st.button(
            "Review notebook", use_container_width=True, key="rev_notebook_btn"
        ):
            st.info("Opening notebook...")


# Initialize decision state if not present
if "courtyard_decision" not in st.session_state:
    st.session_state.courtyard_decision = None


@st.dialog("FINAL DECISION", width="large")
def show_courtyard_decision_modal():
    # -------------------------------------------------------------------------
    # STATE: LOST / UNLOCKED GATE
    # -------------------------------------------------------------------------
    if st.session_state.courtyard_decision == "unlocked":
        st.markdown(
            "<div style='font-size: 22px; font-weight: 700; color: #ffffff; text-align: left; margin-bottom: 20px;'>You opened the gate, Shaden.</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style='background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 14px 16px; margin-bottom: 20px; display: flex; align-items: center; gap: 12px;'>
                <div style='font-size: 24px;'>👤</div>
                <div>
                    <div style='font-size: 13px; font-weight: 600; color: #e2e8f0;'>Fahad — Brother</div>
                    <div style='font-size: 13px; color: #94a3b8; margin-top: 2px;'>Thank you, Shaden.</div>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style='font-size: 14px; color: #cbd5e1; line-height: 1.5; margin-bottom: 24px; padding-bottom: 16px; border-bottom: 1px solid rgba(255, 255, 255, 0.1);'>
                The person outside had Fahad's phone.<br>
                Opening the gate let them inside.
            </div>
        """,
            unsafe_allow_html=True,
        )

        if st.button(
            "Retry final decision",
            type="primary",
            use_container_width=True,
            key="btn_retry_decision",
        ):
            st.session_state.courtyard_decision = None
            st.rerun()

        if st.button(
            "Review evidence",
            use_container_width=True,
            key="btn_review_ev",
        ):
            st.session_state.current_screen = "office"
            st.session_state.active_modal = "evidence"
            st.rerun()

        st.markdown(
            """
            <div style='text-align: center; color: #64748b; font-size: 12px; margin-top: 20px;'>
                — Your puzzles and clues are saved. —
            </div>
        """,
            unsafe_allow_html=True,
        )

    # -------------------------------------------------------------------------
    # STATE: INITIAL DECISION PROMPT
    # -------------------------------------------------------------------------
    else:
        st.markdown("### Someone is waiting outside.")
        st.markdown(
            "<div style='color: #aaaaaa; font-size: 14px; margin-bottom: 20px;'>The key is in your hand, Shaden.</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div style='background: rgba(25, 27, 31, 0.85); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 10px; padding: 12px 16px; margin-bottom: 12px;'>
                <div style='font-size: 13px; font-weight: 600; color: #ffffff;'>👤 Fahad — Brother</div>
                <div style='font-size: 13px; color: #bbbbbb; margin-top: 2px;'>Turn the key, Shaden. I'm right here.</div>
            </div>
            <div style='background: rgba(25, 27, 31, 0.85); border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 10px; padding: 12px 16px; margin-bottom: 12px;'>
                <div style='font-size: 13px; font-weight: 600; color: #ffffff;'>👤 Unknown number</div>
                <div style='font-size: 13px; color: #bbbbbb; margin-top: 2px;'>Shaden, stay inside. We're almost there.</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button(
                "Unlock the gate and leave",
                type="primary",
                use_container_width=True,
                key="btn_unlock",
            ):
                st.session_state.courtyard_decision = "unlocked"
                st.rerun()

        with col2:
            if st.button(
                "Keep the gate locked and wait",
                use_container_width=True,
                key="btn_wait",
            ):
                st.session_state.courtyard_decision = "kept_locked"
                st.rerun()


@st.dialog("Najdi Pattern")
def open_puzzle_1_modal():
    _, col_img, _ = st.columns([1, 2, 1])
    with col_img:
        safe_image("assets/Najd-pattern.png", width=300)

    st.markdown(
        "<div class='clue-caption'>Inspect the traditional geometric wall motif near the door:</div>",
        unsafe_allow_html=True,
    )
    st.markdown("**Puzzle 1:** What is the total sum of triangles pattern?")
    ans1 = st.text_input("Enter the number:", key="m_p1_in").strip()

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "Submit Answer", type="primary", key="p1_sub", use_container_width=True
        ):
            if ans1 == "66":
                st.session_state.game["p1_cleared"] = True
                st.session_state.puzzle_hints["p1_active_level"] = 0
                st.session_state.active_modal = None
                st.success("Correct!")
                time.sleep(0.4)
                st.rerun()
            else:
                st.error("Incorrect answer. Try again.")

    with col2:
        if st.button("Need a Hint?", key="p1_hint_btn", use_container_width=True):
            curr = st.session_state.puzzle_hints.get("p1_active_level", 0)
            if curr < 3:
                st.session_state.puzzle_hints["p1_active_level"] = curr + 1

    p1_hints = {
        1: "Count the number of the triangle in the image.",
        2: "Count the top and lower triangles.",
        3: "Count inner triangles.",
    }
    lvl = st.session_state.puzzle_hints.get("p1_active_level", 0)
    if lvl > 0:
        st.info(f"**Hint {lvl}:** {p1_hints[lvl]}")


@st.dialog("Founding Day")
def open_puzzle_2_modal():
    if not st.session_state.game.get("p1_cleared", False):
        st.warning("Complete Puzzle 1 first!")
        if st.button("Close", key="p2_close", use_container_width=True):
            st.session_state.active_modal = None
            st.rerun()
        return

    st.markdown(
        "<div class='clue-caption'>Inspect the official Saudi Founding Day flag standing on the desk:</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "**Puzzle 2:** What is the Gregorian founding year written in Arabic numerals on the emblem?"
    )
    ans2 = st.text_input("Enter 4-digit year:", key="m_p2_in").strip()

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "Submit Answer", type="primary", key="p2_sub", use_container_width=True
        ):
            if ans2 == "1727":
                st.session_state.game["p2_cleared"] = True
                st.session_state.puzzle_hints["p2_active_level"] = 0
                st.session_state.active_modal = None
                st.success("Correct!")
                time.sleep(0.4)
                st.rerun()
            else:
                st.error("Incorrect year.")

    with col2:
        if st.button("Need a Hint?", key="p2_hint_btn", use_container_width=True):
            curr = st.session_state.puzzle_hints.get("p2_active_level", 0)
            if curr < 3:
                st.session_state.puzzle_hints["p2_active_level"] = curr + 1

    p2_hints = {
        1: "Read the Arabic numerals printed in the emblem.",
        2: "The Hijri year is 1139.",
        3: "Check the image of the founding day.",
    }
    lvl = st.session_state.puzzle_hints.get("p2_active_level", 0)
    if lvl > 0:
        st.info(f"**Hint {lvl}:** {p2_hints[lvl]}")
        if lvl == 3:
            safe_image("assets/Founding_day.jpg", width=320)


@st.dialog("Wall Safe Keypad")
def open_puzzle_3_modal():
    if not st.session_state.game.get("p2_cleared", False):
        st.warning("Complete Puzzle 2 first!")
        if st.button("Close", key="p3_close", use_container_width=True):
            st.session_state.active_modal = None
            st.rerun()
        return

    st.markdown(
        "<div class='clue-caption'>Map Cipher Logbook: Locate landmark codes across the Kingdom grid.</div>",
        unsafe_allow_html=True,
    )
    st.code(
        """
    NEOM (Northwest)        -> Code: 9
    AlUla (West)            -> Code: 4
    Diriyah (Central)       -> Code: 1
    Al Ahsa Oasis (East)    -> Code: 7
    
    Cipher Note: Order location digits by regional 
    coordinate: WEST to EAST.
    """,
        language="text",
    )

    exit_pin = st.text_input(
        "Enter 4-Digit Exit Pin:", max_chars=4, key="m_pin"
    ).strip()

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "Unlock Safe", type="primary", key="p3_sub", use_container_width=True
        ):
            if exit_pin == "4917":
                st.session_state.game["p3_cleared"] = True
                st.session_state.puzzle_hints["p3_active_level"] = 0
                st.session_state.active_modal = None
                st.success("You unlocked the safe!")
                time.sleep(0.4)
                st.rerun()
            else:
                st.error("Incorrect PIN.")

    with col2:
        if st.button("Need a Hint?", key="p3_hint_btn", use_container_width=True):
            curr = st.session_state.puzzle_hints.get("p3_active_level", 0)
            if curr < 3:
                st.session_state.puzzle_hints["p3_active_level"] = curr + 1

    p3_hints = {
        1: "You need the spatial layout of Saudi Arabia. Identify which city is furthest West.",
        2: "Order the locations using the given code.",
        3: "We want to start with the West and end with the East",
    }
    lvl = st.session_state.puzzle_hints.get("p3_active_level", 0)
    if lvl > 0:
        st.info(f"**Hint {lvl}:** {p3_hints[lvl]}")


# -----------------------------------------------------------------------------
# SCREEN RENDERERS
# -----------------------------------------------------------------------------
def render_office_screen():
    solved_count = sum(st.session_state.game.values())

    if solved_count == 3 and st.session_state.active_modal is None:
        st.session_state.active_modal = "evidence"

    if st.session_state.active_modal == "evidence":
        show_evidence_modal()
    elif st.session_state.active_modal == "p1":
        open_puzzle_1_modal()
    elif st.session_state.active_modal == "p2":
        open_puzzle_2_modal()
    elif st.session_state.active_modal == "p3":
        open_puzzle_3_modal()

    img_b64 = load_base64_img("assets/office.jpg")

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

        div[data-testid="stVerticalBlock"] > div:has(div.pin-overlay-1) {{
            position: absolute !important;
            top: 22% !important;
            left: 57% !important;
            z-index: 100 !important;
        }}
        div[data-testid="stVerticalBlock"] > div:has(div.pin-overlay-2) {{
            position: absolute !important;
            top: 57% !important;
            left: 24% !important;
            z-index: 100 !important;
        }}
        div[data-testid="stVerticalBlock"] > div:has(div.pin-overlay-3) {{
            position: absolute !important;
            top: 12% !important;
            left: 44% !important;
            z-index: 100 !important;
        }}

        .stButton > button {{
            background: rgba(18, 18, 20, 0.90) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            border-radius: 20px !important;
            padding: 6px 16px !important;
            font-size: 13px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5) !important;
            transition: all 0.2s ease-in-out !important;
        }}
        .stButton > button:hover {{
            transform: scale(1.08) !important;
            border-color: #ffffff !important;
            background: rgba(30, 30, 35, 0.98) !important;
        }}

        .ev-header-title {{ font-size: 22px; font-weight: 700; color: #ffffff; margin-bottom: 16px; text-align: center; }}
        .ev-subtext {{ font-size: 14px; color: #cccccc; margin-top: 10px; margin-bottom: 16px; text-align: center; }}
        .ev-box {{ background: #191b1f; border: 1px solid #2e323b; border-radius: 8px; padding: 12px 16px; font-size: 13px; color: #e0e0e0; margin-bottom: 12px; }}
        .clue-caption {{ font-size: 13px; color: #aaaaaa; margin-top: 8px; margin-bottom: 12px; font-style: italic; }}
    </style>

    <div class="game-wrapper">
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
    </div>
    """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.markdown("<div class='pin-overlay-1'></div>", unsafe_allow_html=True)
        if st.button("🔴 1. Najdi Pattern", key="btn_p1"):
            st.session_state.active_modal = "p1"
            st.rerun()

    with st.container():
        st.markdown("<div class='pin-overlay-2'></div>", unsafe_allow_html=True)
        if st.button("🔴 2. Founding Flag", key="btn_p2"):
            st.session_state.active_modal = "p2"
            st.rerun()

    with st.container():
        st.markdown("<div class='pin-overlay-3'></div>", unsafe_allow_html=True)
        if st.button("🔴 3. Saudi Image", key="btn_p3"):
            st.session_state.active_modal = "p3"
            st.rerun()


def render_courtyard_screen():
    img_b64 = load_base64_img("assets/outdoor.jpg")

    st.markdown(
        f"""
    <style>
        header[data-testid="stHeader"] {{ display: none !important; }}
        footer {{ visibility: hidden !important; }}
        #MainMenu {{ visibility: hidden !important; }}
        
        .block-container {{ padding: 0rem !important; margin: 0rem !important; max-width: 100% !important; }}
        
        .game-wrapper {{
            position: relative; width: 100vw; height: 100vh;
            background: url('data:image/jpeg;base64,{img_b64}') no-repeat center center;
            background-size: cover; overflow: hidden;
        }}
        .top-bar {{ position: absolute; top: 25px; left: 35px; color: white; }}

        /* 1. Modal Overlay Container: Align to right & remove backdrop dimming */
        div[data-testid="stDialog"] {{
            display: flex !important;
            justify-content: flex-end !important;
            align-items: center !important;
            padding-right: 5vw !important;
            background-color: transparent !important; /* Removes darkened overlay */
        }}

        /* 2. Modal Box Content: Force solid opaque background */
        div[data-testid="stDialog"] > div:first-child {{
            margin: 0 !important;
            transform: none !important;
            max-width: 500px !important;
            width: 100% !important;
            background-color: #18191c !important; /* Fully opaque solid background */
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7) !important;
        }}

        /* 3. Outer Dialog Element Reset */
        div[role="dialog"] {{
            background-color: #18191c !important;
        }}
    </style>

    <div class="game-wrapper">
        <div class="top-bar">
            <div style="font-size: 26px; font-weight: 700;">آخر باب | THE LAST DOOR</div>
            <div style="font-size: 13px; color: #cccccc;">Chapter: Courtyard • Shaden</div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Call dialog AFTER CSS is injected
    show_courtyard_decision_modal()


# -----------------------------------------------------------------------------
# MAIN ROUTER
# -----------------------------------------------------------------------------
if st.session_state.current_screen == "office":
    render_office_screen()
elif st.session_state.current_screen == "courtyard":
    render_courtyard_screen()