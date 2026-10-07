# Display helpers only. The puzzle rules are in room_2.py.
# os finds our files; base64 lets the browser display local pictures.

import os
import base64
import streamlit as st

project_folder = os.path.dirname(os.path.abspath(__file__))

# Main escape_room folder
root_folder = os.path.abspath(
    os.path.join(project_folder, "..", "..")
)

# Room 2 pictures folder
assets_folder = os.path.join(
    root_folder, "assets", "images", "room_2"
)


def picture_data(file_name):
    path = os.path.join(assets_folder, file_name)

    with open(path, "rb") as file:
        picture = file.read()

    return base64.b64encode(picture).decode("utf-8")


def add_style():
    path = os.path.join(project_folder, "room_2_style.css")

    with open(path, "r", encoding="utf-8") as file:
        style = file.read()

    st.markdown("<style>" + style + "</style>", unsafe_allow_html=True)


def show_picture(file_name, x, y, width, height, max_width=360):
    # Show just the close-up part of the original screenshot.
    # The original picture file is kept unchanged.
    picture = picture_data(file_name)
    picture_width = 1672 / width * 100
    picture_left = x / (1672 - width) * 100
    picture_top = y / (941 - height) * 100

    html = f"""
    <div class="puzzle-picture" role="img" aria-label="Puzzle close-up"
         style="width:min(100%, {max_width}px);
                aspect-ratio:{width}/{height};
                background-image:url('data:image/png;base64,{picture}');
                background-size:{picture_width}% auto;
                background-position:{picture_left}% {picture_top}%;
                background-repeat:no-repeat;">
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
