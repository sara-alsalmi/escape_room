# Run this file using: python -m streamlit run app.py
# Streamlit displays the room. room_2.py decides what happens.

import streamlit as st
import navigations
from game.rooms import room_2 as room
from game.rooms import room_2_display as display

# Apply only the Living Room scene and puzzle styles.
# The main app controls the page settings and shared header.

# Streamlit runs this file again after clicks.
# Only create the game when it does not exist yet.
game = None


def setup():
    global game

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
        st.session_state.room = "study"
        st.session_state.page = "message"
        st.rerun()
    else:
        st.warning(message)


# This decorator belongs to Streamlit: it makes a popup window.
@st.dialog("Living room", width="small", on_dismiss=close_popup)
def show_popup(name):
    if name == "Coffee table":
        display.show_picture("coffee_table.png", 362, 254, 611, 506)

        if game["coffee_saved"]:
            st.success("Observation saved.")
        else:
            if st.button("Save observation", type="primary", width="stretch"):
                success, message = room.save_coffee(game)
                if success:
                    navigations.mark_solved("coffee")
                record_feedback(name, success, message)

            show_feedback(name)

    elif name == "Bookshelf":
        display.show_picture("bookshelf.png", 362, 254, 611, 506)

        if game["bookshelf_solved"]:
            st.success("Recovered word: " + game["recovered_word"])
        else:
            answer = st.text_input("Six-letter word", key="word_answer")
            submit_column, hint_column = st.columns(2, gap="small")

            if submit_column.button(
                "Submit", type="primary", key="bookshelf_submit", width="stretch"
            ):
                success, message = room.submit_word(answer, game)
                if success:
                    navigations.mark_solved("bookshelf")
                record_feedback(name, success, message)

            if hint_column.button("Hint", key="bookshelf_hint", width="stretch"):
                st.info(room.get_hint("bookshelf", game))

            show_feedback(name)

    elif name == "Open book":
        display.show_picture("unicode_book.png", 257, 250, 790, 551)

        if game["book_solved"]:
            st.success("PIN recorded in your notebook.")
            if st.button("View page", key="view_book_page", width="stretch"):
                open_popup("Book page")
        else:
            answer = st.text_input("Six-digit PIN", key="book_pin")
            submit_column, hint_column, page_column = st.columns(3, gap="small")

            if submit_column.button(
                "Submit", type="primary", key="book_submit", width="stretch"
            ):
                success, message = room.submit_book_pin(answer, game)
                if success:
                    navigations.mark_solved("book")
                record_feedback(name, success, message)

            if hint_column.button("Hint", key="book_hint", width="stretch"):
                st.info(room.get_hint("book", game))
            if page_column.button("View page", key="view_book_page", width="stretch"):
                open_popup("Book page")

            show_feedback(name)

    elif name == "Book page":
        display.show_picture("unicode_book.png", 257, 250, 790, 551)

        if st.button("Back to puzzle", width="stretch"):
            open_popup("Open book")

    elif name == "Drawer":
        drawer_content = st.empty()

        with drawer_content.container():
            if game["drawer_unlocked"]:
                display.show_picture("drawer_open.png", 364, 253, 576, 487)
            else:
                display.show_picture("drawer_closed.png", 362, 253, 611, 479)

                answer = st.text_input("Six-digit PIN", key="drawer_pin")
                unlock_column, hint_column = st.columns(2, gap="small")

                if unlock_column.button(
                    "Unlock", type="primary", key="drawer_submit", width="stretch"
                ):
                    success, message = room.unlock_drawer(answer, game)

                    if success:
                        navigations.mark_solved("drawer")
                        drawer_content.empty()
                        with drawer_content.container():
                            display.show_picture(
                                "drawer_open.png", 364, 253, 576, 487
                            )

                    record_feedback(name, success, message)

                if hint_column.button("Hint", key="drawer_hint", width="stretch"):
                    st.info(room.get_hint("drawer", game))

        show_feedback(name)

    elif name == "Key found":
        display.show_picture("drawer_open.png", 364, 253, 576, 487)

        if st.button("Save photo", width="stretch"):
            success, message = room.save_photo(game)
            record_feedback(name, success, message)

        show_feedback(name)

    # Like the Basement door, the next-room button appears as soon as the
    # Study key is obtained from the drawer.
    if room.can_enter_study(game):
        if st.button(
            "Go to the study",
            type="primary",
            key="living_go_to_study",
            width="stretch",
        ):
            continue_to_study()

    if st.button("Close", key="close_inspection", width="stretch"):
        close_popup()
        st.rerun()


def progress_text():
    setup()
    return str(room.get_progress(game)) + " / 4 puzzles"


def show_room():
    setup()
    # Apply Living Room styles on every Streamlit rerun
    display.add_style()

    if game["current_room"] == "living_room":
        if st.button("Coffee table", key="hotspot_coffee"):
            open_popup("Coffee table")

        if st.button("Bookshelf", key="hotspot_bookshelf"):
            open_popup("Bookshelf")

        if st.button("Open book", key="hotspot_book"):
            open_popup("Open book")

        if st.button("Drawer", key="hotspot_drawer"):
            open_popup("Drawer")

    else:
        st.success("Living room complete — the study door is unlocked.")
        if st.button("Go to the study", key="hotspot_door"):
            st.session_state.room = "study"
            st.session_state.page = "message"
            st.rerun()

    if st.session_state["popup"] != "":
        show_popup(st.session_state["popup"])
