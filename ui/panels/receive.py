from pathlib import Path

import streamlit as st

from app_config import INBOX_DIR, ENC_SEQ_ID_LEN
from helpers.inbox    import inbox_has_message, clear_inbox
from helpers.rsa_utils import rsa_decrypt_sym_keys
from src.utils.chunk_manager import reassemble_payloads
from src.stego.lsb_engine    import extract_data


def _session_is_active(user: str) -> bool:
    return (
        st.session_state.get("logged_in", False)
        and st.session_state.get("username") == user
        and st.session_state.get("session_token") is not None
        and st.session_state.get("private_key") is not None
        and st.session_state.get("keys_generated", False)
    )

def panel_receive(user: str, partner: str) -> None:
    stage = st.session_state.recv_stage

    st.markdown('<div class="sc-panel">', unsafe_allow_html=True)
    st.markdown('<div class="sc-panel-title">📥 INBOX</div>', unsafe_allow_html=True)

    if stage == "revealed":
        _recv_revealed(user)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    if stage == "inbox_view":
        _recv_inbox_view(user)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    if inbox_has_message(user):
        st.markdown(
            f'<div class="sc-alert sc-alert-warn">'
            f'📨 New encrypted message from <b>{partner}</b>.</div>',
            unsafe_allow_html=True,
        )
        if st.button("📬 CHECK INBOX", width="stretch", key="btn_check_inbox"):
            if not st.session_state.keys_generated:
                st.markdown(
                    '<div class="sc-alert sc-alert-err">⚠ You need your RSA keys to decrypt. Generate them first.</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.session_state.recv_stage = "inbox_view"
                st.rerun()
    else:
        st.markdown(
            '<div class="sc-alert sc-alert-info">No messages in inbox.</div>',
            unsafe_allow_html=True,
        )
        if st.button("🔄 REFRESH", width="stretch", key="btn_refresh"):
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def _recv_inbox_view(user: str) -> None:
    """Show received stego-images and wait for the REVEAL button press."""
    inbox       = INBOX_DIR / user
    stego_files = sorted(inbox.glob("stego_*.png"))

    st.markdown(
        f'<div class="sc-alert sc-alert-info">'
        f'Received <b>{len(stego_files)}</b> stego-image(s).<br>'
        f'Press <b>REVEAL</b> to run RSA decapsulation → ASCON verify → ChaCha20 decrypt.</div>',
        unsafe_allow_html=True,
    )

    if stego_files:
        n_cols = min(len(stego_files), 4)
        cols   = st.columns(n_cols)
        for i, f in enumerate(stego_files):
            with cols[i % n_cols]:
                st.image(str(f), width="stretch")
                st.markdown(
                    f'<div class="sc-img-label">{f.name.upper()}</div>',
                    unsafe_allow_html=True,
                )

    st.markdown('<hr class="sc-divider">', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔓 REVEAL MESSAGE", width="stretch", key="btn_reveal"):
            _do_reveal(user, inbox, stego_files)
    with c2:
        if st.button("← BACK", width="stretch", key="btn_recv_back"):
            st.session_state.recv_stage = None
            st.rerun()


def _do_reveal(user: str, inbox: Path, stego_files: list) -> None:
    """
    Full decryption pipeline:
      1. RSA-OAEP unwrap → recover inner_key, outer_key, ctr_key
      2. LSB extract raw bytes from every stego image
      3. Split raw bytes into enc_seq_id / enc_content
      4. reassemble_payloads → AES-CTR ID sort → ASCON verify → ChaCha20 decrypt
    """
    try:
        if not _session_is_active(user):
            raise RuntimeError("session has ended; sign in again to decrypt messages")

        with st.spinner("🔓 RSA decapsulation & tri-hybrid decryption…"):
            enc_blob = (inbox / "keys.bin").read_bytes()
            inner_key, outer_key, ctr_key = rsa_decrypt_sym_keys(
                enc_blob, st.session_state.private_key
            )

            recovered_payloads = []
            for f in stego_files:
                raw = extract_data(str(f))
                if raw is None:
                    raise ValueError(f"LSB extraction returned nothing for {f.name}")
                enc_seq_id  = raw[:ENC_SEQ_ID_LEN]
                enc_content = raw[ENC_SEQ_ID_LEN:]
                recovered_payloads.append((enc_seq_id, enc_content))

            message = reassemble_payloads(
                recovered_payloads, inner_key, outer_key, ctr_key
            )

        st.session_state.revealed_msg = message
        st.session_state.recv_stage   = "revealed"
        st.rerun()

    except Exception as exc:
        st.markdown(
            f'<div class="sc-alert sc-alert-err">✗ Decryption failed: {exc}</div>',
            unsafe_allow_html=True,
        )


def _recv_revealed(user: str) -> None:
    """Display the decrypted plaintext and offer a CLEAR INBOX action."""
    st.markdown(
        '<div class="sc-alert sc-alert-ok">✓ Integrity verified (ASCON-128). Message successfully decrypted.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="sc-revealed">{st.session_state.revealed_msg}</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="sc-divider">', unsafe_allow_html=True)
    if st.button("🗑 CLEAR INBOX", width="stretch", key="btn_clear_inbox"):
        clear_inbox(user)
        st.session_state.recv_stage   = None
        st.session_state.revealed_msg = None
        st.rerun()
