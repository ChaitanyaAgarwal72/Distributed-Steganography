import streamlit as st

from app_config import PARTNER
from ui.panels.key_status import panel_key_status
from ui.panels.send       import panel_send
from ui.panels.receive    import panel_receive


def screen_dashboard() -> None:
    user    = st.session_state.username
    partner = PARTNER[user]

    hdr_l, hdr_m, hdr_r = st.columns([5, 2, 1])
    with hdr_l:
        st.markdown(
            '<div class="sc-topbar">'
            '<span class="sc-brand">🔐 SecureChat</span>'
            '<span style="color:#334155;font-size:.75rem;font-family:Space Mono,monospace;">'
            'TRI-HYBRID CRYPTO · E2EE · LSB STEGO'
            '</span>'
            '</div>',
            unsafe_allow_html=True,
        )
    with hdr_m:
        st.markdown(
            f'<div style="padding-top:.6rem;text-align:right;">'
            f'<span class="sc-user-badge">● {user.upper()}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    with hdr_r:
        st.write("")
        if st.button("⏻ Logout", width="stretch"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

    key_col, send_col, recv_col = st.columns([1.15, 2.5, 2.5], gap="medium")

    with key_col:
        panel_key_status(user, partner)

    with send_col:
        panel_send(user, partner)

    with recv_col:
        panel_receive(user, partner)
