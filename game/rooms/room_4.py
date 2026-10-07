import html
import streamlit as st

# Courtyard (room 4): the final decision popup and the two endings.


# Final decision popup. Each choice sends the player to an ending page.
@st.dialog("The Gate", width="small", on_dismiss="rerun")
def decision_popup():

    st.markdown("**Would you open the door?**")

    open_col, keep_col = st.columns(2)

    with open_col:
        if st.button("Unlock the gate and leave", key="decision_open", width="stretch"):
            st.session_state.page = "lose"
            st.rerun()

    with keep_col:
        if st.button("Keep the gate locked and wait", type="primary",
                     key="decision_keep", width="stretch"):
            st.session_state.page = "win"
            st.rerun()


# Ending screen. kind is "win" or "lose".
def show_ending(kind):
    # html.escape keeps a strange name from breaking the page
    player = html.escape(st.session_state.player_name)

    if kind == "win":
        title = "The gate stays closed"
        text = ("You step back. The enemy tries the handle, then gives up. "
                "Moments later, help arrives and the person outside is caught. "
                "The evidence mattered.")
        message = f"“{player}, we're here. Keep the gate closed until you hear us.”"
        sender = "Unknown number"
    else:
        title = "You let the enemy in"
        text = ("You turned the key and let the enemy in. "
                "The figure steps through the gate and into the house, "
                "and the door closes behind them. "
                "The voice you trusted was never your brother's.")
        message = f"“Thank you, {player}.”"
        sender = "Fahad — Brother"

    # the losing ending is plain black
    if kind == "lose":
        st.markdown("""
        <style>
        .stApp { background-image: none; background-color: #000000; }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("""
    <style>
    .st-key-ending_panel {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 800px;
        background-color: #1E1814E0;
        padding: 45px 50px;
        border: 1px solid #A68A6E73;
        border-radius: 12px;
        box-shadow: 0 0 40px #000000CC;
    }
    .ending_title {
        font-size: 40px;
        font-family: Times New Roman, serif;
        letter-spacing: 5px;
        text-transform: uppercase;
        color: #e9e5dc;
        margin-bottom: 20px;
    }
    .ending_text {
        font-size: 22px;
        font-family: Times New Roman, serif;
        color: #e9e5dc;
        line-height: 1.5;
        margin-bottom: 30px;
    }
    .ending_msg {
        background-color: #2a211c;
        border: 1px solid #FFFFFF26;
        border-radius: 10px;
        padding: 20px;
        color: #e9e5dc;
        font-size: 18px;
    }
    .ending_sender {
        font-size: 12px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: #c9b8a8;
        margin-bottom: 10px;
    }
    .st-key-ending_panel .stButton button {
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
    </style>
    """, unsafe_allow_html=True)

    with st.container(key="ending_panel"):
        st.markdown(f"""
        <div class="ending_title">{title}</div>
        <div class="ending_text">{text}</div>
        <div class="ending_msg">
            <div class="ending_sender">{sender}</div>
            {message}
        </div>
        """, unsafe_allow_html=True)

        if st.button("Play again", width="stretch"):
            st.session_state.clear()
            st.query_params.clear()
            st.rerun()