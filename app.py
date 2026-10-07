import html
import streamlit as st
import navigations
import room_1
import room_3
import room_4
from story import Story


# Settings
st.set_page_config(page_title="The Last Door", page_icon="🚪", layout="wide")

# Removes the default header since it's not used in the project
st.markdown("""
<style>
[data-testid="stHeader"] { display: none; }
footer { display: none; }
</style>
""", unsafe_allow_html=True)

# Prepare the saved values (a refresh restores them from the URL)
navigations.setup()
room_1.setup()
room_3.setup()
room_1.apply_style()


# Save the current values in the address
navigations.save_to_url()

# Used by every room page
def set_background(file_name):
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("app/static/{file_name}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)


def room_header(name, progress):
    st.markdown(f"""
    <style>
    .room_title {{
        position: fixed;
        top: 40px;
        left: 64px;
        color: #e9e5dc;
    }}
    .room_name {{
        font-size: 42px;
        font-family: Times New Roman, serif;
        letter-spacing: 6px;
        text-transform: uppercase;
        margin: 0;
    }}
    .room_progress {{
        font-size: 14px;
        letter-spacing: 4px;
        text-transform: uppercase;
        color: #c9b8a8;
        margin-top: 8px;
    }}
    </style>

    <div class="room_title">
        <div class="room_name">{name}</div>
        <div class="room_progress">{progress}</div>
    </div>
    """, unsafe_allow_html=True)



# Interface 1: introduction
if st.session_state.page == "name":

    set_background("intro.jpeg")

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


# Interface 2: messages (one screen before each room)
if st.session_state.page == "message":

    # read this room's text (html.escape keeps a strange name from breaking the page)
    player = html.escape(st.session_state.player_name)
    room = st.session_state.room
    story = Story(player).get(room)

    set_background(story["background"])

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

        st.markdown(f"""
        <div class="message_text">{story["text"]}</div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="msg_panel">
                <div class="msg_sender">Fahad — Brother</div>
                <div class="msg_text">{story["fahad"]}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="msg_panel">
                <div class="msg_sender">Unknown number</div>
                <div class="msg_text">{story["unknown"]}</div>
            </div>
            """, unsafe_allow_html=True)

        # start button, goes to the room 
        if st.button(story["button"], width="stretch"):
            st.session_state.page = room
            st.rerun()

    # the Phone reads the messages from story.py by itself
    navigations.show_navigations()
    st.stop()


# interface Basement (dark): the only thing to click is the electrical box
if st.session_state.page == "basement":

    set_background("Basement_dark.jpeg")
    room_header("Basement", navigations.progress_text("basement"))
    navigations.show_navigations()

    st.markdown("""
    <style>
    /* where the button sits on the room */
    .st-key-hotspot_kit {
        position: fixed;
        top: 330px;
        left: 680px;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("Electricity", key="hotspot_kit"):
        room_1.generator_popup()

    st.stop()


# interface Basement lit: boxes, mirror, key cabinet, then the door
if st.session_state.page == "basement2":

    set_background("Basement.jpeg")
    room_header("Basement", navigations.progress_text("basement"))
    navigations.show_navigations()

    st.markdown("""
    <style>
    .st-key-hotspot_boxes {
        position: fixed;
        top: 600px;
        left: 300px;
    }
    .st-key-hotspot_mirror {
        position: fixed;
        top: 350px;
        left: 900px;
    }
    .st-key-hotspot_key {
        position: fixed;
        top: 400px;
        right: 500px;
    }
    .st-key-hotspot_door {
        position: fixed;
        top: 300px;
        right: 150px;
    }
    .st-key-hotspot_door button {
        opacity: 0;
        width: 150px;
        height: 250px;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

    # Each hotspot opens its popup, the popup code lives in room_1.py
    if st.button("Storage boxes", key="hotspot_boxes"):
        room_1.boxes_popup()

    if st.button("Mirror", key="hotspot_mirror"):
        room_1.mirror_popup()

    if st.button("Key cabinet", key="hotspot_key"):
        room_1.key_popup()

    # the door only appears after the key is found
    if navigations.is_solved("key"):
        if st.button("Open door", key="hotspot_door"):
            st.session_state.room = "majlis"
            st.session_state.page = "message"
            st.rerun()

    st.stop()

# interface Study: three puzzles, then the safe opens the way to the courtyard
if st.session_state.page == "study":
 
    set_background("study.jpeg")
    room_header("Study", navigations.progress_text("study"))
    navigations.show_navigations()
 
    st.markdown("""
    <style>
    .st-key-hotspot_najdi {
        position: fixed;
        top: 22%;
        left: 57%;
    }
    .st-key-hotspot_flag {
        position: fixed;
        top: 57%;
        left: 24%;
    }
    .st-key-hotspot_safe {
        position: fixed;
        top: 12%;
        left: 44%;
    }
    .st-key-hotspot_exit {
        position: fixed;
        bottom: 60px;
        left: 50%;
        transform: translateX(-50%);
    }
    </style>
    """, unsafe_allow_html=True)
 
    # Each hotspot opens its popup, the popup code lives in room_3.py
    if st.button("Najdi pattern", key="hotspot_najdi"):
        room_3.najdi_popup()
 
    if st.button("Founding flag", key="hotspot_flag"):
        room_3.founding_popup()
 
    if st.button("Saudi picture", key="hotspot_safe"):
        room_3.safe_popup()
 
 
    st.stop()
 
if st.session_state.page == "courtyard":

    set_background("Courtyard.jpeg")
    room_header("Courtyard", "Final decision")
    navigations.show_navigations()

    st.markdown("""
    <style>
    .st-key-hotspot_gate {
        position: fixed;
        top: 40%;
        left: 50%;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("The gate", key="hotspot_gate"):
        room_4.decision_popup()

    st.stop()


# Endings: "win" (kept the gate closed) and "lose" (opened it)
if st.session_state.page in ("win", "lose"):

    if st.session_state.page == "win":
        set_background("Courtyard_dark.jpeg")

    room_4.show_ending(st.session_state.page)
    st.stop()
 
# Majlis / Courtyard: placeholders until these rooms are built
# page: (title, background, next room)
PLACEHOLDERS = {
    "majlis": ("Majlis", "Majlis_dark.jpeg", "study"),
}
 
if st.session_state.page in PLACEHOLDERS:
    title, background, next_room = PLACEHOLDERS[st.session_state.page]
 
    set_background(background)
 
    if next_room is None:
        room_header(title, "Final decision coming soon")
    else:
        room_header(title, navigations.progress_text(st.session_state.page))
 
    # temporary: go to the next room
    if next_room is not None and st.button("Next (temporary)", key="next_btn"):
        st.session_state.room = next_room
        st.session_state.page = "message"
        st.rerun()
 
    navigations.show_navigations()
    st.stop()
