import streamlit as st
from pathlib import Path
from story import Story
from game.rooms import room_2_display as room_2_display

# Folder of the project, so file paths work wherever the app is started from
BASE = Path(__file__).resolve().parent

# Every screen the game has, and the order of the rooms
PAGES = [
    "name", "message", "basement", "basement2", "majlis", "study",
    "courtyard", "win", "lose",
]
ROOMS = ["basement", "majlis", "study", "courtyard"]


def setup():
    # Read saved game information from the URL, to allow  restore its state after a page refresh.
    if "page" not in st.session_state:
        page = st.query_params.get("page", "name")
        room = st.query_params.get("room", "basement")
        name = st.query_params.get("name", "")
        solved_text = st.query_params.get("solved", "")

        solved = solved_text.split(",") if solved_text else []

        # Store the current game state 
        st.session_state.page = page
        st.session_state.room = room
        st.session_state.player_name = name
        st.session_state.solved = solved

 # Save the current game state in the URL so it can be restored after a refresh.
def save_to_url():
    st.query_params["page"] = st.session_state.page
    st.query_params["room"] = st.session_state.room
    st.query_params["name"] = st.session_state.player_name
    st.query_params["solved"] = ",".join(st.session_state.solved)


# Solved puzzles functions to keep track of progress
ROOM_PUZZLES = {
    "basement": ["generator", "boxes", "mirror", "key"],
    "majlis": ["coffee", "bookshelf", "book", "drawer"],
    "study": ["najdi", "founding", "safe"],
    "courtyard": [],
}

def mark_solved(puzzle):
    if puzzle not in st.session_state.solved:
        st.session_state.solved.append(puzzle)

def is_solved(puzzle):
    return puzzle in st.session_state.solved


def progress_text(room):
    done = 0
    for puzzle in ROOM_PUZZLES[room]:
        if is_solved(puzzle):
            done += 1
    total = len(ROOM_PUZZLES[room])
    return f"{done} / {total} puzzles"


# Map navigation as saved picture for each room
All_Maps = {
    "basement": "Basement_map.png",
    "majlis": "Majilis_map.png",
    "study": "Study_map.png",
    "courtyard": "Courtyard_map.png",
}

@st.dialog("Map", width="medium")
def show_map():
    path = BASE / "static" / All_Maps[st.session_state.room]
    st.image(str(path))



# Phone navigation
# Messages are read from story.py: all rooms up to the current one.
@st.dialog("Phone", width="medium")
def show_phone():
    story = Story(st.session_state.player_name)
    last = ROOMS.index(st.session_state.room)

    for room in ROOMS[:last + 1]:
        messages = story.get(room)
        for sender, key in [("Fahad — Brother", "fahad"), ("Unknown number", "unknown")]:
            st.markdown(f"**{sender}**")
            st.write(messages[key])
            st.divider()


#  Notebook 
# for each solved puzzle
CLUES = {
    "generator": ("basement", "The generator is running."),
    "boxes": ("basement", "The boxes gave you the code 951."),
    "mirror": ("basement", "Reverse what you found."),
    "key": ("basement", "You found the basement key."),
    "coffee": ("majlis", "Coffee table note"),
    "bookshelf": ("majlis", "Bookshelf word: INSIDE"),
    "book": ("majlis", "Book PIN: 383389"),
    "drawer": ("majlis", "Item found: Study key"),
    "najdi": ("study", "Najdi pattern result: 66"),
    "founding": ("study", "Founding year: 1727"),
    "safe": ("study", "Safe PIN: 4917 — courtyard key found"),
}

@st.dialog("Notebook", width="medium")
def show_notebook():
    current_room = st.session_state.room

    for puzzle, (room, clue) in CLUES.items():
        if room == current_room and is_solved(puzzle):
            st.write(clue)
            if puzzle == "coffee":
                room_2_display.show_picture(
                    "coffee_table.png", 362, 254, 611, 506, max_width=220
                )


# The three buttons 
def show_navigations():
    st.markdown("""
    <style>
    .st-key-nav {
        position: fixed;
        top: 30px;
        right: 40px;
        width: 420px;
        z-index: 999;
    }

    .st-key-nav button {
        font-size: 0;
        color: transparent;
        background-color: #8a9a86;
        border: none;
        height: 60px;
    }

    .st-key-nav_map button {
        background-image: url("app/static/location.png");
        background-size: 40px;
        background-position: center;
        background-repeat: no-repeat;
    }

    .st-key-nav_notebook button {
        background-image: url("app/static/notes.png");
        background-size: 40px;
        background-position: center;
        background-repeat: no-repeat;
    }

    .st-key-nav_phone button {
        background-image: url("app/static/smartphone.png");
        background-size: 40px;
        background-position: center;
        background-repeat: no-repeat;
    }
    </style>
    """, unsafe_allow_html=True)

    with st.container(key="nav"):
        col1, col2, col3 = st.columns(3)
        if col1.button("Map", key="nav_map", width="stretch"):
            show_map()
        if col2.button("Notebook", key="nav_notebook", width="stretch"):
            show_notebook()
        if col3.button("Phone", key="nav_phone", width="stretch"):
            show_phone()
