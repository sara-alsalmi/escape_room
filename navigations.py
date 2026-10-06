import streamlit as st

# Setup for the navigation values through the game
def setup():
    if "room" not in st.session_state:
        st.session_state.room = "basement"
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "clues" not in st.session_state:
        st.session_state.clues = {}

# Saved picture for each room room
All_Maps = {
    "basement": "static/Basement_map.png",
    "majlis": "static/Majlis_map.png",
    "study": "static/Study_map.png",
    "courtyard":"static/Courtyard_map.png",
}

@st.dialog("Map")
def show_map():
    st.image(All_Maps[st.session_state.room])

# Save the messages shown in a room so player can see them
def add_message(sender, text):
    if (sender, text) not in st.session_state.messages:
        st.session_state.messages.append((sender, text))

# Show the messages seen yet 
@st.dialog("Phone")
def show_phone():
    if not st.session_state.messages:
        st.write("No messages yet.")
    for sender, text in st.session_state.messages:
        st.markdown(f"**{sender}**")
        st.write(text)
        st.divider()

# Save the solved answer so the Notebook can show it
# After use : navigation.add_clue("basement", "Lantern", 4) 
def add_clue(room, label, value):
    st.session_state.clues.setdefault(room, {})[label] = value

# Show the solved puzzles  
@st.dialog("Notebook")
def show_notebook():
    if not st.session_state.clues:
        st.write("No clues saved yet.")
    for room, clues in st.session_state.clues.items():
        st.subheader(room.title())
        for label, value in clues.items():
            st.write(f"{label} = {value}")

# For the three buttons that will be shown for the navigations
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
    background-color: transparent;
    background-color: #e9e5dc;
    border: none;
    height: 60px;
    }

    .st-key-nav_map button {
    background-image: url("static/location.png");
    background-size: 40px;
    background-position: center;
    }
    
    .st-key-nav_notebook button {
    background-image: url("static/notes.png");
    background-size: 40px;
    background-position: center;
    }
    
    .st-key-nav_phone button {
    background-image: url("static/smartphone.png");
    background-size: 40px;
    background-position: center;
    }

    </style>
    """, unsafe_allow_html=True)

    with st.container(key="nav"):
        col1, col2, col3 = st.columns(3)
        if col1.button("Map", key="nav_map", use_container_width=True):
            show_map()
        if col2.button("Notebook", key="nav_notebook", use_container_width=True):
            show_notebook()
        if col3.button("Phone", key="nav_phone", use_container_width=True):
            show_phone()