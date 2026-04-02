import streamlit as st
from secrets import token_hex


def init_state() -> None:
    """
    Populate st.session_state with default values on first run.
    Keys already present are left untouched (safe to call on every rerun).
    """
    defaults: dict = {
        "logged_in":      False,
        "username":       None,
        "session_token":  None,

        "private_key":    None,
        "keys_generated": False,

        "send_stage":     None,
        "stego_paths":    [],
        "enc_sym_keys":   None,

        "recv_stage":     None,
        "revealed_msg":   None,
    }
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


def start_user_session(username: str) -> None:
    """Mark the current browser session as authenticated for one user."""
    st.session_state.logged_in = True
    st.session_state.username = username
    st.session_state.session_token = token_hex(16)


def end_user_session() -> None:
    """Invalidate all sensitive state for the active browser session."""
    st.session_state.clear()
