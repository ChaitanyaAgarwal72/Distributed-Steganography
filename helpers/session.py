import streamlit as st


def init_state() -> None:
    """
    Populate st.session_state with default values on first run.
    Keys already present are left untouched (safe to call on every rerun).
    """
    defaults: dict = {
        "logged_in":      False,
        "username":       None,

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
