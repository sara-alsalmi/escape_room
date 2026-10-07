import streamlit as st
from pathlib import Path
import time

# Python script for the basement room: all related functions (puzzles) and the page interface 

# ------------------------------------ Puzzle Functions (Logic part) ------------------------------------

# 1. First puzzle 
# Power generator puzzle function 
# The user needs to activate all five switches to turn on the power.

# List to store the correct sequence of turning the switches on (correct is: switch 3, 1, 4, 2, then 5)
correct_switches_order = [3, 1, 4, 2, 5]

# A list to save the player's order for turning the Switch on.
current_switches_order = []

# Turn on the switch if it is the correct next switch 
def turn_switch(switches, correct_switches_order, current_switches_order, switch_number):

    # If the switch chosed by player is the correct one add it to the current_order list 
    if switch_number == correct_switches_order[len(current_switches_order)] : 
        switches[switch_number - 1] = True # Turn the switch to True 
        current_switches_order.append(switch_number) # Append to the current switches order list
        return True
    # Return False 
    return False


# Reset function that reset all generator's switches to off (False)
def reset_generator():
    return [False for x in range(5)]

# 2. Second puzzle 
# The other puzzle is finding the correct answer to the equations (the player should enter three correct numbers)

# Tuple to store the counts of the shapes
shapes_counts = (3, 3, 3, 2)

shape1_count =  shapes_counts[0] # Hilal icon (outlined)
shape2_count =  shapes_counts[1] # Hilal icon (filled)
shape3_count = shapes_counts[2] # star icon (filled)
shape4_count = shapes_counts[3] # Sun icon (outlined)

answers = []

answers.append(shape1_count * shape3_count)
answers.append(shape4_count + shape2_count)
answers.append(shape3_count - shape4_count)

answers = tuple(answers)

# Check player answer
def check_answer(player_answer):

    for i in range(3):
        if player_answer[i] != answers[i]:
            return False
    return True


# 3. Third puzzle 
# Mirror puzzle function 

# The puzzle here is that the mirrors consist of three vertical segments; 
# the player must adjust them so they all face the right direction, 
# revealing a phrase that helps with the final solution.


# 
mirror_parts_status = [False, True, False]

def rotate_mirror(mirror_parts_status, mirror_number):
    if mirror_parts_status[mirror_number - 1] == True:
        mirror_parts_status[mirror_number - 1] = not True 
    else : 
        mirror_parts_status[mirror_number - 1] = True   

def check_mirror(mirror_parts_status): 
    for i in mirror_parts_status:
        if i == False :
            return False 
    return True

def return_rotation_angle(mirror_parts_status, mirror_number): 
    if mirror_parts_status[mirror_number - 1] == True:
        return 0
    else : 
        return 180 

# 4. Final Puzzle (KEY CABINET)
# Function to check if player get the correct code to open the KEY CABINET to get the key
def check_code(player_code):
    if player_code == "159":
        return True 
    else: 
        return False 

# ------------------------------------ Interface Part (Streamlit) ------------------------------------

# Streamlit session stat for retaining values ​​between reruns for the same user

# Store the switches state
if "switches" not in st.session_state:
    st.session_state.switches = reset_generator()

# Store the player's current order
if "current_order" not in st.session_state:
    st.session_state.current_order = []

# Store whether the player selected a wrong switch
if "wrong_switch" not in st.session_state:
    st.session_state.wrong_switch = False

# Store the status of the mirrors 
if "mirror_parts_status" not in st.session_state: 
    st.session_state.mirror_parts_status = [False, True, False]

# Store whether the generator popup is open 
if "generator_open" not in st.session_state:
    st.session_state.generator_open = False

# Store whether the boxes popen is open 
if "boxes_open" not in st.session_state:
    st.session_state.boxes_open = False

# Store whether the mirror popen is open 
if "mirror_open" not in st.session_state:
    st.session_state.mirror_open = False

# Store whether the mirror popen is open 
if "key_open" not in st.session_state:
    st.session_state.key_open = False

if "key_cabinet_opened" not in st.session_state:
    st.session_state.key_cabinet_opened = False


# Styling the popup 

st.markdown(
    """
    <style>

    /* Start Generator button */
    div[data-testid="stDialog"] button[kind="primary"] {
        background-color: #5f6959;
        color: #f1eee6;
        border: 1px solid #747f6d;
        border-radius: 8px;
    }

    /* Start Generator hover */
    div[data-testid="stDialog"] button[kind="primary"]:hover {
        background-color: #6c7765;
        color: #ffffff;
        border-color: #899482;
    }

    /* Normal buttons inside the popup */
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

def close_generator_popup():
    st.session_state.generator_open = False

def close_boxes_popup():
    st.session_state.boxes_open = False

def close_mirror_popup():
    st.session_state.mirror_open = False

def close_key_popup():
    st.session_state.key_open = False

# Generator Popup Interface  
@st.dialog("Emergency Generator", width="small", on_dismiss=close_generator_popup)
def generator_popup():

    # Friendly caption to the player 
    st.caption(
        "The power is off. Find the correct startup sequence."
    )

    # Root path 
    ROOT = Path(__file__).resolve().parents[2]
    
    # Generator and note image
    st.image(
        str(ROOT / "assets" / "images" / "room_1" / "generator_note_puzzle.png"),
        use_container_width=True
    )

    # Display a wrong message if the chosen switch is wrong (If Wrong Switch = True then display error message)
    if st.session_state.wrong_switch:

        st.error("Wrong sequence. The switches have reset.")
        st.session_state.wrong_switch = False


    # Switch buttons 

    switch_columns = st.columns(5)

    switch_numbers = ["1", "2", "3", "4", "5"]


    for i, column in enumerate(switch_columns):

        with column:

            is_on = st.session_state.switches[i]

            st.markdown(
                f"<div style='text-align:center;'>Switch {switch_numbers[i]}</div>",
                unsafe_allow_html=True
            )

            if st.button( 
                "ON" if is_on else "OFF",
                icon=":material/toggle_on:" if is_on else ":material/toggle_off:",
                key=f"switch_{i + 1}",
                use_container_width=True,
                disabled=is_on
                ):
                
                correct = turn_switch(
                    st.session_state.switches,
                    correct_switches_order,
                    st.session_state.current_order,
                    i + 1
                )


                # Reset if the player selects the wrong switch
                if correct == False:

                    st.session_state.switches = reset_generator()
                    st.session_state.current_order = []
                    st.session_state.wrong_switch = True

                # Not refresh the page 
                st.rerun(scope="fragment")


    st.caption(
        "Follow the note and activate the switches in the correct order."
    )


    # Start generator button 

    if st.button(
        "Start generator",
        type="primary",
        icon=":material/power_settings_new:",
        use_container_width=True
    ):

        if all(st.session_state.switches):

            # Display success message and after 2 seconds close the popup
            st.success("Correct order! The generator is running.")
            time.sleep(2)
            # Set generator_open = False to close the popup 
            st.session_state.generator_open = False
            st.rerun()

        else:

            st.error("It didn't start. Complete the startup sequence first.")


    # Reset button 

    if st.button(
        "Reset switches",
        icon=":material/restart_alt:",
        use_container_width=True
    ):

        st.session_state.switches = reset_generator()
        st.session_state.current_order = []
        st.session_state.wrong_switch = False

        st.rerun(scope="fragment")



# Boxes Popup Interface 
@st.dialog("Storage Boxes", width="small", on_dismiss=close_boxes_popup)
def boxes_popup():

    # Friendly caption to the player
    st.caption(
        "Check the inspection labels and solve the equations."
    )
    # Root path 
    ROOT = Path(__file__).resolve().parents[2]
    
    # Boxes and note image
    st.image(
        str(ROOT / "assets" / "images" / "room_1" / "boxes_note_puzzle.png"),
        use_container_width=True
    )

    # Player inputs
    input_columns = st.columns(3)

    with input_columns[0]:
        answer_1 = st.text_input("Number 1")
        
    with input_columns[1]:
        answer_2 = st.text_input("Number 2")
        
    with input_columns[2]:
        answer_3 = st.text_input("Number 3")

    # Submit button
    if st.button(
        "Submit",
        type="primary",
        icon=":material/arrow_forward:",
        use_container_width=True
    ):

        # First check if user entered all answers or not 
        if not (answer_1.isdigit() and answer_2.isdigit() and answer_3.isdigit()):
            st.error("Enter the full three answers.")

        else :
            player_answer = (int(answer_1), int(answer_2), int(answer_3))

            if check_answer(player_answer):

                st.success("Correct answer. You solved the puzzle")
                time.sleep(2)
                st.session_state.boxes_open = False
                st.rerun()
            else:
                st.error("Incorrect. Check the labels and try again.")


# Mirror Popup Interface  
@st.dialog("Mirror", width="small", on_dismiss=close_mirror_popup)
def mirror_popup(): 
    # Friendly caption to the player
    st.caption("The reflection doesn't look right.")

    # Root path 
    ROOT = Path(__file__).resolve().parents[2]

    # Display the solved mirror
    if check_mirror(st.session_state.mirror_parts_status):

        # Smooth reveal animation
        st.markdown(
            """
            <style>
            @keyframes mirror_reveal {
                from {
                    opacity: 0;
                    transform: scale(0.97);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }

            div[data-testid="stDialog"] [data-testid="stImage"] img {
                animation: mirror_reveal 0.5s ease-out;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.image(str(ROOT / "assets" / "images" / "room_1" / "mirror_wholePart.png"),use_container_width=True)

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

        return

    # Set three columns for each part of the mirror 
    col1, col2, col3 = st.columns(3, gap="small")

    with col1: 
        display_mirror_image(ROOT / "assets" / "images" / "room_1" / "mirror_part_1.png",1)
        if st.button("Rotate", icon=":material/rotate_right:", key="mirror_button_1", use_container_width=True):
            rotate_mirror(st.session_state.mirror_parts_status, 1)
            st.rerun(scope="fragment")

    with col2: 
        display_mirror_image(ROOT / "assets" / "images" / "room_1" / "mirror_part_2.png",2)
        if st.button("Rotate", icon=":material/rotate_right:", key="mirror_button_2", use_container_width=True):
            rotate_mirror(st.session_state.mirror_parts_status, 2)
            st.rerun(scope="fragment")

    
    with col3: 
        display_mirror_image(ROOT / "assets" / "images" / "room_1" / "mirror_part_3.png",3)
        if st.button("Rotate", icon=":material/rotate_right:", key="mirror_button_3", use_container_width=True):
            rotate_mirror(st.session_state.mirror_parts_status, 3)
            st.rerun(scope="fragment")


# Key Cabinet Popup Interface  
@st.dialog("Key Cabinet", width="small", on_dismiss=close_key_popup)
def key_popup(): 
    # Friendly caption to the player
    st.caption(
        "A three-digit lock secures the cabinet."
    )

    # Root path 
    ROOT = Path(__file__).resolve().parents[2]
        
    left, center, right = st.columns([1, 1.5, 1])
    
    #with center:
    #    st.image(str(ROOT / "assets" / "images" / "room_1" / "key_cabinet.png"),width=210)
    with center:
        if st.session_state.key_cabinet_opened:
            st.image(str(ROOT / "assets" / "images" / "room_1" / "key.png"),width=250)
        else:
            st.image(str(ROOT / "assets" / "images" / "room_1" / "key_cabinet.png"),width=250)

    # Set three columns for each input code from the player 
    col1, col2, col3 = st.columns(3, gap="small")

    with col1: 
        digit_1 = st.text_input("",placeholder="—", 
                                max_chars=1, 
                                key="key_digit_1",
                                label_visibility="collapsed")

    with col2: 
        digit_2 = st.text_input("",placeholder="—", 
                                max_chars=1, 
                                key="key_digit_2",
                                label_visibility="collapsed")

    with col3: 
        digit_3 = st.text_input("",placeholder="—", 
                                max_chars=1, 
                                key="key_digit_3",
                                label_visibility="collapsed")

    st.markdown(":material/lightbulb: Use what you discovered in the basement.",text_alignment="center")

    # Concatenate the digits entered by player 
    str_code = digit_1 + digit_2 + digit_3

    # Store True or False 
    code_correct = check_code(str_code)

    open_cabinet_button, back_button = st.columns([1.35, 1],gap="small")

    with open_cabinet_button:
        open_cabinet_button = st.button("Open cabinet", type="primary", use_container_width=True)
    
    with back_button:
        back_button = st.button("Back",use_container_width=True)
    
    if open_cabinet_button:
        if not (digit_1.isdigit() and digit_2.isdigit() and digit_3.isdigit()):
            st.error("Enter the full three-digit code.")
        elif code_correct:
            #st.success("The cabinet unlocks.")
            st.session_state.key_cabinet_opened = True
            st.rerun(scope="fragment")
        else:
            st.error("Incorrect code. Try again.")
    
    if back_button:
        st.session_state.key_open = False
        st.rerun()

    if st.session_state.key_cabinet_opened:
        st.success("The cabinet unlocks. You found the basement key.")

    


# Helper function (to display the mirror parts)
def display_mirror_image(image_path, mirror_number):
    import base64
    rotation_angle = return_rotation_angle(
        st.session_state.mirror_parts_status, mirror_number
    )

    # Convert the image to Base64 to use in HTML 
    with open(image_path, "rb") as image_file:
        image_html = base64.b64encode(image_file.read()).decode("utf-8")

    # Display the image with the correct rotation 
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
        
    

# Basement Page (Just sample for now to test the puzzles)
st.title("Basement")


if st.button("Start generator puzzle"):
    st.session_state.generator_open = True

# Reopen the popup after each rerun
if st.session_state.generator_open:
    generator_popup()

if st.button("Start boxes puzzle"):
    st.session_state.boxes_open = True

if st.session_state.boxes_open:
    boxes_popup()

if st.button("Start mirror puzzle"):
    st.session_state.mirror_open = True

if st.session_state.mirror_open:
    mirror_popup()

if st.button("Start key cabinet"):
    st.session_state.key_open = True

if st.session_state.key_open:
    key_popup()