# Run this file using: python -m streamlit run app.py
# Streamlit displays the room. room_2.py decides what happens.

import streamlit as st
import room_2 as room
import display

st.set_page_config(page_title="The Last Door — Living Room", layout="wide",
                   initial_sidebar_state="collapsed")
display.add_style()

# Streamlit runs this file again after clicks.
# Only create the game when it does not exist yet.
if "game" not in st.session_state:
    st.session_state["game"] = room.new_game()
if "popup" not in st.session_state:
    st.session_state["popup"] = ""
if "feedback" not in st.session_state:
    st.session_state["feedback"] = {}
if "player_name" not in st.session_state:
    st.session_state["player_name"] = "Shaden"

game = st.session_state["game"]


def close_popup():
    st.session_state["popup"] = ""


def open_popup(name):
    st.session_state["popup"] = name
    st.rerun()


def record_feedback(name, success, message):
    st.session_state["feedback"][name] = [success, message]
    st.rerun()


def show_feedback(name):
    if name in st.session_state["feedback"]:
        success, message = st.session_state["feedback"][name]

        if success:
            st.success(message)
        else:
            st.warning(message)


def restart_level():
    st.session_state["game"] = room.new_game()
    st.session_state["popup"] = ""
    st.session_state["feedback"] = {}

    # Clear old typed answers as well as the completed milestones.
    for key in ["word_answer", "book_pin", "drawer_pin"]:
        if key in st.session_state:
            del st.session_state[key]


def continue_to_study():
    success, message = room.enter_study(game)

    if success:
        st.session_state["popup"] = ""
        st.rerun()
    else:
        st.warning(message)


# This decorator belongs to Streamlit: it makes a popup window.
@st.dialog("Living room", width="large", on_dismiss=close_popup)
def show_popup(name):
    if name == "Coffee table":
        picture, controls = st.columns([1.65, 1])

        with picture:
            display.show_picture("coffee_table.png", 362, 254, 611, 506)
        with controls:
            st.subheader("Coffee table")
            st.write("Coffee has soaked into the napkin.")
            st.write("The charging cable has no phone attached.")
            st.write("The chair is pushed back.")

            if st.button("Save observation", type="primary"):
                success, message = room.save_coffee(game)
                record_feedback(name, success, message)

            show_feedback(name)

    elif name == "Bookshelf":
        picture, controls = st.columns([1.65, 1])

        with picture:
            display.show_picture("bookshelf.png", 362, 254, 611, 506)
        with controls:
            st.subheader("Between the books")
            st.write("Use the bookmark numbers to take one letter from each title.")
            st.write("Count letters starting at 1.")
            st.caption("Left to right: 2 · 1 · 1 · 2 · 1 · 1")

            if game["bookshelf_solved"]:
                st.success("Recovered word: " + game["recovered_word"])
            else:
                with st.form("bookshelf_form"):
                    answer = st.text_input("Six-letter word", key="word_answer")
                    submitted = st.form_submit_button("Submit", type="primary")

                if submitted:
                    success, message = room.submit_word(answer, game)
                    record_feedback(name, success, message)

            if st.button("Hint", key="bookshelf_hint"):
                st.info(room.get_hint("bookshelf", game))

            show_feedback(name)

    elif name == "Open book":
        picture, controls = st.columns([1.75, 1])

        with picture:
            display.show_picture("unicode_book.png", 257, 250, 790, 551)
        with controls:
            st.subheader("Characters and numbers")

            if game["bookshelf_solved"]:
                st.write("Recovered word: " + game["recovered_word"])
            else:
                st.info("Recover the word from the bookshelf first.")

            st.write("Use the book page to work out the drawer PIN.")
            st.caption("One digit per letter. Keep the last digit.")

            if game["book_solved"]:
                st.success("PIN recorded in your notebook.")
            else:
                with st.form("book_form"):
                    answer = st.text_input("Six-digit PIN", key="book_pin")
                    submitted = st.form_submit_button("Submit", type="primary")

                if submitted:
                    success, message = room.submit_book_pin(answer, game)
                    record_feedback(name, success, message)

            if st.button("Hint", key="book_hint"):
                st.info(room.get_hint("book", game))
            if st.button("View page"):
                open_popup("Book page")

            show_feedback(name)

    elif name == "Book page":
        st.subheader("Python Fundamentals — Characters and numbers")
        display.show_picture("unicode_book.png", 257, 250, 790, 551)

        with st.expander("Readable letter table"):
            st.table({"Letter": list(room.letter_codes.keys()),
                      "Code": list(room.letter_codes.values())})

        if st.button("Back to puzzle"):
            open_popup("Open book")

    elif name == "Drawer":
        if game["drawer_unlocked"]:
            open_popup("Key found")

        picture, controls = st.columns([1.65, 1])

        with picture:
            display.show_picture("drawer_closed.png", 362, 253, 611, 479)
        with controls:
            st.subheader("Study key drawer")
            st.write("Enter the PIN you worked out from the programming book.")

            with st.form("drawer_form"):
                answer = st.text_input("Six-digit PIN", key="drawer_pin")
                submitted = st.form_submit_button("Unlock drawer", type="primary")

            if submitted:
                success, message = room.unlock_drawer(answer, game)

                if success:
                    open_popup("Key found")
                else:
                    record_feedback(name, success, message)

            if st.button("Notebook", key="drawer_notebook"):
                open_popup("Notebook")
            if st.button("Hint", key="drawer_hint"):
                st.info(room.get_hint("drawer", game))

            show_feedback(name)

    elif name == "Key found":
        picture, controls = st.columns([1.65, 1])

        with picture:
            display.show_picture("drawer_open.png", 364, 253, 576, 487)
        with controls:
            st.subheader("Study key found")
            st.write("The study key is inside.")
            st.write("A family photograph lies beneath it.")

            if st.button("Continue to study", type="primary", key="reward_continue"):
                continue_to_study()
            if st.button("Save photograph"):
                success, message = room.save_photo(game)
                record_feedback(name, success, message)

            show_feedback(name)

    elif name == "Notebook":
        st.subheader("Notebook")

        if len(game["notebook"]) == 0:
            st.write("Your notebook is empty.")
        else:
            for clue, text in game["notebook"].items():
                st.markdown("**" + room.clue_names[clue] + "**")
                st.write(text)

                if clue == "photo":
                    display.show_picture("drawer_open.png", 364, 253, 576, 487)

        st.divider()
        st.write("Inventory")

        if "study_key" in game["inventory"]:
            st.write("Study key")
        else:
            st.write("No items collected yet.")

        if game["drawer_unlocked"]:
            if st.button("Back to drawer"):
                open_popup("Key found")

    elif name == "Map":
        st.subheader("House map")
        st.write("Basement → Living room → Study → Courtyard")
        st.write("You are in the living room.")

        if room.can_enter_study(game):
            st.success("The study is available.")
            if st.button("Continue to study", key="map_continue"):
                continue_to_study()
        else:
            st.write("The study is locked.")

    elif name == "Phone":
        st.subheader("Phone")

        if len(game["phone_messages"]) == 0:
            st.write("No new messages.")
        else:
            for message in game["phone_messages"]:
                st.write(message)

    st.divider()
    if st.button("Close", key="close_inspection"):
        close_popup()
        st.rerun()


with st.sidebar:
    st.write("Player settings")
    st.text_input("Player name", key="player_name")
    st.caption("Progress is kept during this play session.")
    st.button("Restart level", on_click=restart_level)

heading, navigation = st.columns([1.4, 1])

with heading:
    st.markdown('<h1 class="game-title" dir="rtl" style="text-align:left">آخر باب</h1>',
                unsafe_allow_html=True)
    st.markdown('<div class="english-title">THE LAST DOOR · A HOUSE IN RIYADH</div>',
                unsafe_allow_html=True)
    st.caption("Chapter 2 · Living room")
    st.write(st.session_state["player_name"])

with navigation:
    map_column, notebook_column, phone_column, progress_column = st.columns(4)

    with map_column:
        if st.button("Map", use_container_width=True):
            open_popup("Map")
    with notebook_column:
        if st.button("Notebook", use_container_width=True):
            open_popup("Notebook")
    with phone_column:
        if st.button("Phone", use_container_width=True):
            open_popup("Phone")
    with progress_column:
        st.write(str(room.get_progress(game)) + " / 4")
        st.caption("complete")

if game["current_room"] == "living_room":
    with st.container(key="room_scene"):
        if st.button("1  Coffee table", key="hotspot_coffee"):
            open_popup("Coffee table")
        if st.button("2  Bookshelf", key="hotspot_bookshelf"):
            open_popup("Bookshelf")
        if st.button("3  Open book", key="hotspot_book"):
            open_popup("Open book")
        if st.button("4  Drawer", key="hotspot_drawer"):
            open_popup("Drawer")

    st.caption("Inspect the room. Save observations and work out the drawer PIN.")
else:
    st.success("Living room complete — the study door is unlocked.")
    st.write("This local version ends here. Your key and notebook are ready for the next room.")

    if st.button("Return to living room"):
        game["current_room"] = "living_room"
        st.rerun()

if st.session_state["popup"] != "":
    show_popup(st.session_state["popup"])
