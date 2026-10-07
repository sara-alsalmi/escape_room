import base64
import time
from pathlib import Path
import streamlit as st
import navigations

# Basement room: puzzle logic (plain Python) + the popups .

# Folder of this room's pictures
IMAGES = Path(__file__).resolve().parent / "assets" / "images" / "room_1"

# ------------------------------------ Puzzle Functions (Logic part) ------------------------------------

# 1. Generator puzzle: turn on the five switches in the right order
correct_switches_order = [3, 1, 4, 2, 5] # List to store the correct sequen

# Turn the switch on only if it is the correct next switch
def turn_switch(switches, correct_switches_order, current_switches_order, switch_number):

    if switch_number == correct_switches_order[len(current_switches_order)] : 
        switches[switch_number - 1] = True # Turn the switch to True 
        current_switches_order.append(switch_number) # Append to the current switches order list
        return True
    return False

# Turn all generator switches off
def reset_generator():
    return [False for x in range(5)]


# 2. Boxes puzzle: three equations from the shapes
# Counts: hilal outlined, hilal filled, star filled, sun outlined
shapes_counts = (3, 3, 3, 2)

shape1_count = shapes_counts[0] # Hilal icon (outlined)
shape2_count = shapes_counts[1] # Hilal icon (filled)
shape3_count = shapes_counts[2] # star icon (filled)
shape4_count = shapes_counts[3] # Sun icon (outlined)


answers = (
    shape1_count * shape3_count,   # 9
    shape4_count + shape2_count,   # 5
    shape3_count - shape4_count,   # 1
)

# Check player answer
def check_answer(player_answer):
    for i in range(3):
        if player_answer[i] != answers[i]:
            return False
    return True


# 3. Mirror puzzle: three parts, each facing right (True) or upside down (False) revealing a phrase that helps with the final solution.
def rotate_mirror(mirror_parts_status, mirror_number):
    mirror_parts_status[mirror_number - 1] = not mirror_parts_status[mirror_number - 1]

def check_mirror(mirror_parts_status):
    for i in mirror_parts_status:
        if i == False:
            return False
    return True

def return_rotation_angle(mirror_parts_status, mirror_number):
    if mirror_parts_status[mirror_number - 1] == True:
        return 0
    return 180


# 4. Key cabinet: the code is the boxes answers (951) reversed
def check_code(player_code):
    return player_code == "159"


# ------------------------------------ Interface Part (Streamlit) ------------------------------------

# Create the room's values. Called by app_try.py on EVERY run (safe to repeat),
# so a refresh can never leave a value missing.
def setup():
    if "switches" not in st.session_state:
        st.session_state.switches = reset_generator()

    if "current_order" not in st.session_state:
        st.session_state.current_order = []

    if "wrong_switch" not in st.session_state:
        st.session_state.wrong_switch = False

    if "mirror_parts_status" not in st.session_state:
        if navigations.is_solved("mirror"):
            st.session_state.mirror_parts_status = [True, True, True]
        else:
            st.session_state.mirror_parts_status = [False, True, False]


# Style of the popups
def apply_style():
    st.markdown(
        """
        <style>
        div[data-testid="stDialog"] button[kind="primary"] {
            background-color: #5f6959;
            color: #f1eee6;
            border: 1px solid #747f6d;
            border-radius: 8px;
        }
        div[data-testid="stDialog"] button[kind="primary"]:hover {
            background-color: #6c7765;
            color: #ffffff;
            border-color: #899482;
        }
        div[data-testid="stDialog"] button[kind="secondary"] {
            border-radius: 8px;
        }
        div[data-testid="stDialog"] .stButton > button {
            min-height: 48px;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# Show a picture of this room 
def show_image(file_name, width="stretch"):
    path = IMAGES / file_name
    if path.exists():
        st.image(str(path), width=width)
    else:
        st.warning(f"Missing picture: {file_name}")


# for ref:  to open a popup (from app_try.py):
# if st.button("Storage boxes", key="hotspot_boxes"):
#         room_1.boxes_popup()
# on_dismiss="rerun" refreshes the page when the player closes the popup with X.

# Generator popup
@st.dialog("Emergency Generator", width="large", on_dismiss="rerun")
def generator_popup():
    st.caption("The power is off. Find the correct startup sequence.")

    show_image("generator_note_puzzle.png")

    # Show a message if the last switch was wrong
    if st.session_state.wrong_switch:
        st.error("Wrong sequence. The switches have reset.")
        st.session_state.wrong_switch = False

    switch_columns = st.columns(5)

    for i, column in enumerate(switch_columns):
        with column:
            is_on = st.session_state.switches[i]

            st.markdown(
                f"<div style='text-align:center;'>Switch {i + 1}</div>",
                unsafe_allow_html=True
            )

            if st.button(
                "ON" if is_on else "OFF",
                icon=":material/toggle_on:" if is_on else ":material/toggle_off:",
                key=f"switch_{i + 1}",
                width="stretch",
                disabled=is_on
            ):
                correct = turn_switch(
                    st.session_state.switches,
                    correct_switches_order,
                    st.session_state.current_order,
                    i + 1
                )

                # Wrong switch: reset everything
                if correct == False:
                    st.session_state.switches = reset_generator()
                    st.session_state.current_order = []
                    st.session_state.wrong_switch = True

                # Refresh only the popup
                st.rerun(scope="fragment")

    st.caption("Follow the note and activate the switches in the correct order.")

    if st.button(
        "Start generator",
        type="primary",
        icon=":material/power_settings_new:",
        width="stretch"
    ):
        if all(st.session_state.switches):
            st.success("Correct order! The generator is running.")
            time.sleep(2)
            navigations.mark_solved("generator")
            st.session_state.page = "basement2"
            st.rerun()
        else:
            st.error("It didn't start. Complete the startup sequence first.")

    if st.button(
        "Reset switches",
        icon=":material/restart_alt:",
        width="stretch"
    ):
        st.session_state.switches = reset_generator()
        st.session_state.current_order = []
        st.session_state.wrong_switch = False
        st.rerun(scope="fragment")


# Boxes popup
@st.dialog("Storage Boxes", width="large", on_dismiss="rerun")
def boxes_popup():
    st.caption("Check the inspection labels and solve the equations.")

    show_image("boxes_note_puzzle.png")

    input_columns = st.columns(3)
    with input_columns[0]:
        answer_1 = st.text_input("Number 1")
    with input_columns[1]:
        answer_2 = st.text_input("Number 2")
    with input_columns[2]:
        answer_3 = st.text_input("Number 3")

    if st.button(
        "Submit",
        type="primary",
        icon=":material/arrow_forward:",
        width="stretch"
    ):
        answer_1 = answer_1.strip()
        answer_2 = answer_2.strip()
        answer_3 = answer_3.strip()

        if not (answer_1.isdigit() and answer_2.isdigit() and answer_3.isdigit()):
            st.error("Enter the full three answers.")
        elif check_answer((int(answer_1), int(answer_2), int(answer_3))):
            st.success("Correct answer. You solved the puzzle")
            time.sleep(2)
            navigations.mark_solved("boxes")
            st.rerun()
        else:
            st.error("Incorrect. Check the labels and try again.")


# Mirror popup
@st.dialog("Mirror", width="large", on_dismiss="rerun")
def mirror_popup():
    st.caption("The reflection looks wrong. Rotate the mirror pieces until the word becomes readable.")

    columns = st.columns(3, gap="small")

    for i, column in enumerate(columns):
        number = i + 1
        with column:
            display_mirror_image(IMAGES / f"mirror_part_{number}.png", number)
            if st.button("Rotate", icon=":material/rotate_right:",
                         key=f"mirror_button_{number}", width="stretch"):
                rotate_mirror(st.session_state.mirror_parts_status, number)
                st.rerun(scope="fragment")

    if check_mirror(st.session_state.mirror_parts_status):
        navigations.mark_solved("mirror")
        st.html(
            """
            <div style="
                width: 100%;
                box-sizing: border-box;
                margin-top: 16px;
                padding: 14px 18px;
                text-align: center;
                background: #5f6959;
                color: #f1eee6;
                border: 1px solid #747f6d;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                letter-spacing: 0.08em;
            ">
                REVERSE WHAT YOU FOUND TO OPEN THE KEY CABINET
            </div>
            """
        )


# Key cabinet popup
@st.dialog("Key Cabinet", width="small", on_dismiss="rerun")
def key_popup():
    st.caption("A three-digit lock secures the cabinet.")

    cabinet_opened = navigations.is_solved("key")

    left, center, right = st.columns([1, 1.5, 1])
    with center:
        if cabinet_opened:
            show_image("key.png", width=250)
        else:
            show_image("key_cabinet.png", width=250)

    col1, col2, col3 = st.columns(3, gap="small")
    with col1:
        digit_1 = st.text_input("Digit 1", placeholder="—", max_chars=1,
                                key="key_digit_1", label_visibility="collapsed")
    with col2:
        digit_2 = st.text_input("Digit 2", placeholder="—", max_chars=1,
                                key="key_digit_2", label_visibility="collapsed")
    with col3:
        digit_3 = st.text_input("Digit 3", placeholder="—", max_chars=1,
                                key="key_digit_3", label_visibility="collapsed")

    st.markdown(":material/lightbulb: Use what you discovered in the basement.",
                text_alignment="center")

    str_code = digit_1 + digit_2 + digit_3

    open_column, back_column = st.columns([1.35, 1], gap="small")
    with open_column:
        open_clicked = st.button("Open cabinet", type="primary", width="stretch")
    with back_column:
        back_clicked = st.button("Back", width="stretch")

    if open_clicked:
        if not (digit_1.isdigit() and digit_2.isdigit() and digit_3.isdigit()):
            st.error("Enter the full three-digit code.")
        elif check_code(str_code):
            navigations.mark_solved("key")
            st.rerun(scope="fragment")
        else:
            st.error("Incorrect code. Try again.")

    if back_clicked:
        st.rerun()

    if cabinet_opened:
        st.success("The cabinet unlocks. You found the basement key.")


# Show a mirror part, turned the right way
def display_mirror_image(image_path, mirror_number):
    if not Path(image_path).exists():
        st.warning(f"Missing picture: {Path(image_path).name}")
        return

    rotation_angle = return_rotation_angle(
        st.session_state.mirror_parts_status, mirror_number
    )

    with open(image_path, "rb") as image_file:
        image_html = base64.b64encode(image_file.read()).decode("utf-8")

    st.html(
        f"""
        <img
            src="data:image/png;base64,{image_html}"
            style="
                width: 100%;
                height: auto;
                display: block;
                transform: rotate({rotation_angle}deg);
            "
        >
        """
    )

