import streamlit as st
import navigations
from story import Story
from game.rooms import room_1 


# Settings 
st.set_page_config(page_title="The Last Door", page_icon="🚪", layout="wide")

# Removes the defualt header since its not used in the project 
st.markdown("""
<style>
[data-testid="stHeader"] { display: none; }
footer { display: none; }
</style>
""", unsafe_allow_html=True)

# create the navigations for rooms
navigations.setup()

# remember the screen after a refresh -
# first run of a session: read the screen from the address (URL)
if "page" not in st.session_state:
    st.session_state.page = st.query_params.get("page", "name")
    st.session_state.room = st.query_params.get("room", "basement")
    st.session_state.player_name = st.query_params.get("name", "")

# no name saved means the player skipped the first screen, so go back to it
if st.session_state.page != "name" and st.session_state.player_name == "":
    st.session_state.page = "name"

# every run: save the current screen in the address
st.query_params["page"] = st.session_state.page
st.query_params["room"] = st.session_state.room
st.query_params["name"] = st.session_state.player_name

#---------------------------------------------------------

# Interface 1: introduction 
if st.session_state.page == "name":

    # Background photo
    st.markdown("""<style>
    .stApp {
        background-image: url("app/static/intro.jpeg");
        background-size: cover;
        background-position: center;
    }
    </style>""", unsafe_allow_html=True)

    # Title format and style
    st.markdown("""<style>
    .title {
        position: fixed;
        top: 170px;
        right: 100px;
        color: #7b695c;
        text-align: right;
    }
    .arabic {
        font-size: 70px;
        font-weight: bold;
        font-family: Times New Roman, Cario, serif;
        margin: 0;
    }
    .english {
        font-size: 35px;
        font-weight: bold;
        font-family: Times New Roman, serif;
        margin: 0;
        letter-spacing: 4.5px;
    }
    </style>""", unsafe_allow_html=True)

    st.markdown("""<div class="title">
        <div class="arabic">آخـــــــر بـــــاب</div>
        <div class="english">THE LAST DOOR</div>
    </div>""", unsafe_allow_html=True)

    # Name entry panel format and style
    st.markdown("""<style>
    .st-key-name_panel {
        position: fixed;
        width: 700px;
        top: 500px;
        right: 250px;
        background-color: #4a3f38;
        padding: 40px;
        color: white;
        border: 1px solid #FFFFFF33;
        border-radius: 12px;
        box-shadow: 0 10px 30px #00000059;
    }
    .name_text {
        font-size: 35px;
        font-weight: bold;
        font-family: Times New Roman, serif;
        color: white;
    }
    .st-key-name_panel .stButton button {
        width: 100%;
        background-color: #8a9a86;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 20px;
    }
    </style>""", unsafe_allow_html=True)

    with st.container(key="name_panel"):
        st.markdown('<div class="name_text">Someone knows your name.</div>',
                    unsafe_allow_html=True)
        name = st.text_input("Enter Your First Name")

        if st.button("Begin"):
            try:
                name = name.strip()
                if name == "":
                    raise ValueError("Please enter your first name.")

                st.session_state.player_name = name
                st.session_state.page = "message"
                st.rerun()

            except ValueError as e:
                st.error(str(e))
    st.stop()

# Interface 2: messages
if st.session_state.page == "message":

    #  read this room's text
    player = st.session_state.player_name
    room = st.session_state.room
    story = Story(player).get(room)

    # background changes per room
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("app/static/{story["background"]}");
        background-size: cover;
        background-position: center;
    }}
    </style>
    """, unsafe_allow_html=True)

    # style of the panel 
    st.markdown("""
    <style>

    .st-key-message_panel {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 900px;
        background-color: #1E1814E0;
        padding: 45px 50px;
        border: 1px solid #A68A6E73;
        border-radius: 12px;
        box-shadow: 0 0 40px #000000CC;
    }

    .message_text {
        font-size: 22px;
        font-family: Times New Roman, serif;
        color: #e9e5dc;
        line-height: 1.5;
        margin-bottom: 30px;
    }

    .msg_panel {
        background-color: #2a211c;
        border: 1px solid #FFFFFF26;
        border-radius: 10px;
        padding: 20px;
        color: #e9e5dc;
        min-height: 140px;
    }

    .msg_sender {
        font-size: 12px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #c9b8a8;
        margin-bottom: 10px;
    }

    .msg_text {
        font-size: 18px;
        line-height: 1.4;
    }

    .st-key-message_panel .stButton button {
        background-color: #8a9a86;
        color: white;
        border: none;
        border-radius: 8px;
        height: 52px;
        font-size: 18px;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-top: 20px;
    }

    .st-key-message_panel .stButton button:hover {
        background-color: #9fb09b;
        box-shadow: 0 0 18px #8A9A8699;
    }

    </style>
    """, unsafe_allow_html=True)

    with st.container(key="message_panel"):

        # story paragraph
        st.markdown(f"""
        <div class="message_text">{story["text"]}</div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        # Fahad's message
        with col1:
            st.markdown(f"""
            <div class="msg_panel">
                <div class="msg_sender">Fahad — Brother</div>
                <div class="msg_text">{story["fahad"]}</div>
            </div>
            """, unsafe_allow_html=True)

        # unknown number's message
        with col2:
            st.markdown(f"""
            <div class="msg_panel">
                <div class="msg_sender">Unknown number</div>
                <div class="msg_text">{story["unknown"]}</div>
            </div>
            """, unsafe_allow_html=True)

        # start button 
        if st.button(story["button"], use_container_width=True):
            st.session_state.page = room
            st.rerun()
       

    # save the two messages so the Phone can show them
    navigations.add_message("Fahad — Brother", story["fahad"])
    navigations.add_message("Unknown number", story["unknown"])
    navigations.show_navigations()
    st.stop()
    
 #  Basement 
if st.session_state.page == "basement":
    navigations.show_navigations()
#if "solved" not in st.session_state:
#st.session_state.solved = []
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("app/static/Basement_dark.jpeg");
        background-size: cover;
    }}
    </style>
    """, unsafe_allow_html=True)


    st.markdown("""
    <style>
    .room_title {
        position: fixed;
        top: 40px;
        left: 64px;
        color: #e9e5dc;
    }

    .room_name {
        font-size: 42px;
        font-family: Times New Roman, serif;
        letter-spacing: 6px;
        text-transform: uppercase;
        margin: 0;
    }

    .room_progress {
        font-size: 14px;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: #c9b8a8;
        margin-top: 8px;
    }

    /* where the button sits on the room */
    .st-key-hotspot_kit {
        position: fixed;
        top: 330px;
        right: 500px;
    }
    </style>

    <div class="room_title">
        <div class="room_name">Basement</div>
        <div class="room_progress">0 / 4 puzzles</div>
    </div>
    """, unsafe_allow_html=True)

    # the button
    if st.button("Electrical box", key="hotspot_kit"):
        room_1.generator_popup()

    st.stop()

if "key_obtained" not in st.session_state:
    st.session_state.key_obtained = False
if st.session_state.page == "basement2":

    navigations.show_navigations()

    # Background
    st.markdown("""
    <style>
    .stApp {
        background-image: url("app/static/Basement.jpeg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    .room_title {
        position: fixed;
        top: 40px;
        left: 64px;
        color: #e9e5dc;
    }

    .room_name {
        font-size: 42px;
        font-family: Times New Roman, serif;
        letter-spacing: 6px;
        text-transform: uppercase;
        margin: 0;
    }

    .room_progress {
        font-size: 14px;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: #c9b8a8;
        margin-top: 8px;
    }

    /* Boxes hotspot */
    .st-key-hotspot_boxes {
        position: fixed;
        top: 600px;
        left: 300px;
    }

    /* Mirror hotspot */
    .st-key-hotspot_mirror {
        position: fixed;
        top: 350px;
        left: 900px;
    }

    /* Key cabinet hotspot */
    .st-key-hotspot_key {
        position: fixed;
        top: 400px;
        right: 500px;
    }
    .st-key-hotspot_door {
    position: fixed;
    top: 300px;
    right: 150px
    }
    
    .st-key-hotspot_door button {
    opacity: 0;
    width: 150px;
    height: 250px;
    cursor: pointer;
    }


    </style>

    <div class="room_title">
        <div class="room_name">Basement</div>
        <div class="room_progress">1 / 4 puzzles</div>
    </div>
    """, unsafe_allow_html=True)


    # BOXES HOTSPOT
    if st.button("Storage boxes",key="hotspot_boxes"):
        st.session_state.boxes_open = True

    if st.session_state.boxes_open:
        room_1.boxes_popup()


    # MIRROR HOTSPOT
    if st.button("Mirror",key="hotspot_mirror"):
        st.session_state.mirror_open = True

    if st.session_state.mirror_open:
        room_1.mirror_popup()


    # KEY CABINET HOTSPOT

    if st.button("Key cabinet", key="hotspot_key"):
        st.session_state.key_open = True

    if st.session_state.key_open:
        room_1.key_popup()


    if st.session_state.key_obtained:
        if st.button("Open door", key="hotspot_door"):
            st.session_state.room = "majlis"
            st.session_state.page = "message"
            st.rerun()


    st.stop()


# Study
if st.session_state.page == "study":

    st.markdown("""
    <style>
    .stApp {
        background-image: url("app/static/Study_dark.jpeg");
        background-size: cover;
        background-position: center;
    }
    </style>

    <div class="room_title">
        <div class="room_name">Study</div>
        <div class="room_progress">0 / 4 puzzles</div>
    </div>
    """, unsafe_allow_html=True)

    # temporary: go to the next room
    if st.button("Next (temporary)", key="next_btn"):
        st.session_state.room = "courtyard"
        st.session_state.page = "message"
        st.rerun()


    navigations.show_navigations()
    st.stop()


# Courtyard (placeholder so the last Start button has somewhere to go)
if st.session_state.page == "courtyard":

    st.markdown("""
    <style>
    .stApp {
        background-image: url("app/static/Courtyard_dark.jpeg");
        background-size: cover;
        background-position: center;
    }
    </style>

    <div class="room_title">
        <div class="room_name">Courtyard</div>
        <div class="room_progress">Final decision coming soon</div>
    </div>
    """, unsafe_allow_html=True)

    navigations.show_navigations()
    st.stop()
