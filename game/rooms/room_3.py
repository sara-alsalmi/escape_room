import time
from pathlib import Path
import streamlit as st
import navigations

# Study room (room 3): puzzle logic (plain Python) + the popups.
# The page itself (background, hotspots) lives in app_try.py, like room 1.

# Folder of this room's pictures
IMAGES = Path(__file__).resolve().parents[2] / "assets" / "images" / "room_3"

#  Puzzle Functions (Logic part) 

# 1. Najdi pattern solution
najdi_answer = "66"

def check_najdi(player_answer):
    return player_answer == najdi_answer


# 2. Founding Day flag solution
founding_year = "1727"

def check_founding(player_answer):
    return player_answer == founding_year


# 3. Wall safe solution
safe_pin = "4917"

def check_safe(player_pin):
    return player_pin == safe_pin


# Hints (neutral: they only explain the puzzle, they never push toward a sender)
HINTS = {
    "najdi": [
        "Count the number of the triangle in the image.",
        "Count the top and lower triangles.",
        "Count inner triangles.",
    ],
    "founding": [
        "Read the Arabic numerals printed in the emblem.",
        "The Hijri year is 1139.",
        "Check the image of the founding day.",
    ],
    "safe": [
        "You need the spatial layout of Saudi Arabia. Identify which city is furthest West.",
        "Order the locations using the given code.",
        "We want to start with the West and end with the East.",
    ],
}

# The message found inside the safe 
SAVED_MESSAGE = ("Saved message: \"I lost my..... \"")


#  Interface Part (Streamlit) 

# Create the room's values. Called by app_try.py on EVERY run (safe to repeat).
def setup():
    if "room3_hints" not in st.session_state:
        st.session_state.room3_hints = {"najdi": 0, "founding": 0, "safe": 0}


# Show a picture of this room
def show_image(file_name, width="stretch"):
    path = IMAGES / file_name
    if path.exists():
        st.image(str(path), width=width)
    else:
        st.warning(f"Missing picture: {file_name}")


# The "Need a hint?" button: shows one more hint each click (max 3)
def hint_button(puzzle):
    if st.button("Need a hint?", key=f"hint_btn_{puzzle}", width="stretch"):
        level = st.session_state.room3_hints[puzzle]
        if level < len(HINTS[puzzle]):
            st.session_state.room3_hints[puzzle] = level + 1


def show_hint(puzzle):
    level = st.session_state.room3_hints[puzzle]
    if level > 0:
        st.info(f"**Hint {level}:** {HINTS[puzzle][level - 1]}")


# Shown when the player opens a puzzle before the previous one is solved
def locked_message(previous_name):
    st.warning(f"Solve the {previous_name} first.")
    if st.button("Close", key="locked_close", width="stretch"):
        st.rerun()


# Puzzle 1 Najdi Pattern: Player counts the triangles in the wall pattern.
@st.dialog("Najdi Pattern", width="small", on_dismiss="rerun")
def najdi_popup():
    if navigations.is_solved("najdi"):
        st.success("Solved. The pattern gave you the number 66.")
        return

    st.caption("Inspect the traditional geometric wall motif near the door.")

    _, center, _ = st.columns([1, 2, 1])
    with center:
        show_image("Najd-pattern.png", width=300)

    st.markdown("**Puzzle 1:** What is the total?")
    answer = st.text_input("Enter the number:", key="najdi_input").strip()

    submit_col, hint_col = st.columns(2)
    with submit_col:
        if st.button("Submit", type="primary", key="najdi_submit", width="stretch"):
            if check_najdi(answer):
                st.success("Correct!")
                time.sleep(1)
                navigations.mark_solved("najdi")
                st.rerun()
            else:
                st.error("Incorrect answer. Try again.")
    with hint_col:
        hint_button("najdi")

    show_hint("najdi")


# Puzzle 2 Founding Day: Player reads the Gregorian founding year from the Saudi Founding Day emblem.
@st.dialog("Founding Day", width="small", on_dismiss="rerun")
def founding_popup():
    if navigations.is_solved("founding"):
        st.success("Solved. The flag shows the year 1727.")
        return

    if not navigations.is_solved("najdi"):
        locked_message("Najdi pattern")
        return

    st.caption("Inspect the official Saudi Founding Day flag standing on the desk.")
    st.markdown("**Puzzle 2:** What is the Gregorian founding year written in Arabic numerals on the emblem?")
    answer = st.text_input("Enter the 4-digit year:", max_chars=4, key="founding_input").strip()

    submit_col, hint_col = st.columns(2)
    with submit_col:
        if st.button("Submit", type="primary", key="founding_submit", width="stretch"):
            if check_founding(answer):
                st.success("Correct!")
                time.sleep(1)
                navigations.mark_solved("founding")
                st.rerun()
            else:
                st.error("Incorrect year.")
    with hint_col:
        hint_button("founding")

    show_hint("founding")

    # The last hint also shows the picture
    if st.session_state.room3_hints["founding"] == 3:
        show_image("Founding_day.jpg", width=320)


# Puzzle 3 Wall Safe Keypad: Player uses the codes from four Saudi locations and orders them from West to East.
@st.dialog("Wall Safe Keypad", width="small", on_dismiss="rerun")
def safe_popup():
    # Already open: show what is inside
    if navigations.is_solved("safe"):
        st.success("The safe is open. Inside: the security tablet and the courtyard key.")
        show_image("security_footage.jpeg")
        st.caption("Security footage")
        st.info(SAVED_MESSAGE)
        if st.button("Go to the courtyard", type="primary", key="safe_continue", width="stretch"):
            st.session_state.room = "courtyard"
            st.session_state.page = "message"
            st.rerun()
        return

    if not navigations.is_solved("founding"):
        locked_message("Founding Day flag")
        return
    st.caption("Map Cipher Logbook: locate the landmark codes across the Kingdom.")
    st.code("""
Diriyah        = Code: 1
Jeddah         = Code: 4
NEOM           = Code: 9
Al Ahsa Oasis  = Code: 7

Cipher Note: Order the location digits WEST to EAST.
""", language="text")

    pin = st.text_input("Enter the 4-digit exit PIN:", max_chars=4, key="safe_input").strip()

    submit_col, hint_col = st.columns(2)
    with submit_col:
        if st.button("Unlock safe", type="primary", key="safe_submit", width="stretch"):
            if check_safe(pin):
                navigations.mark_solved("safe")
                st.rerun(scope="fragment")   # reopen the popup, now showing the safe's content
            else:
                st.error("Incorrect PIN.")
    with hint_col:
        hint_button("safe")

    show_hint("safe")
