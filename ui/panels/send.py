import shutil
import tempfile
from io       import BytesIO
from pathlib  import Path

import streamlit as st
from PIL import Image
from Crypto.Random import get_random_bytes

from app_config import STAGING_DIR, INBOX_DIR
from helpers.rsa_utils import load_public_keys, rsa_encrypt_sym_keys
from src.utils.chunk_manager import split_and_prepare_payloads
from src.stego.lsb_engine    import embed_data

def panel_send(user: str, partner: str) -> None:
    stage = st.session_state.send_stage

    st.markdown('<div class="sc-panel">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="sc-panel-title">📡 TRANSMIT → {partner.upper()}</div>',
        unsafe_allow_html=True,
    )

    if stage == "sent":
        st.markdown(
            f'<div class="sc-alert sc-alert-ok">'
            f'✓ Stego-images delivered to <b>{partner}</b>\'s inbox.<br>'
            f'Symmetric keys are RSA-sealed. Only {partner} can open.</div>',
            unsafe_allow_html=True,
        )
        if st.button("↩ Compose New Message", width="stretch", key="btn_new_msg"):
            st.session_state.send_stage   = None
            st.session_state.stego_paths  = []
            st.session_state.enc_sym_keys = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    if stage == "preview":
        _send_preview(partner)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    _compose_form(user, partner)
    st.markdown('</div>', unsafe_allow_html=True)


def _compose_form(user: str, partner: str) -> None:
    keys_gen      = st.session_state.keys_generated
    public_keys   = load_public_keys()
    partner_ready = partner in public_keys

    if not keys_gen:
        st.markdown(
            '<div class="sc-alert sc-alert-warn">⚠ Generate your RSA keys first (Key Status panel).</div>',
            unsafe_allow_html=True,
        )
    if not partner_ready:
        st.markdown(
            f'<div class="sc-alert sc-alert-warn">⚠ Waiting for {partner} to generate their keys.</div>',
            unsafe_allow_html=True,
        )

    if not (keys_gen and partner_ready):
        return

    message  = st.text_area(
        "Secret message",
        placeholder="Type your secure message…",
        height=110,
        key="inp_message",
    )
    uploaded = st.file_uploader(
        "Cover images (PNG / JPG)",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="up_covers",
        help="Upload one image per message chunk. More images = finer distribution.",
    )

    can_send = bool(message and message.strip() and uploaded)

    if st.button(
        "🔐 ENCRYPT & TRANSMIT",
        width="stretch",
        disabled=not can_send,
        key="btn_encrypt",
    ):
        _do_encrypt_stage(user, partner, message.strip(), uploaded, public_keys[partner])


def _do_encrypt_stage(
    user:            str,
    partner:         str,
    message:         str,
    uploaded_files,
    partner_pub_pem: str,
) -> None:
    """Run the full tri-hybrid encryption + LSB stego pipeline and stage results."""
    num_parts = len(uploaded_files)

    inner_key = get_random_bytes(32)   # ChaCha20
    outer_key = get_random_bytes(16)   # ASCON-128
    ctr_key   = get_random_bytes(16)   # AES-128-CTR (seq IDs)

    enc_sym_keys = rsa_encrypt_sym_keys(inner_key, outer_key, ctr_key, partner_pub_pem)

    stage_sub   = Path(tempfile.mkdtemp(dir=STAGING_DIR))
    cover_paths = []
    for i, uf in enumerate(uploaded_files):
        suffix = Path(uf.name).suffix or ".png"
        p = stage_sub / f"cover_{i}{suffix}"
        p.write_bytes(uf.read())
        cover_paths.append(str(p))

    stego_dir = stage_sub / "stego"
    stego_dir.mkdir()

    try:
        with st.spinner(f"🔐 Encrypting & embedding into {num_parts} image(s)…"):
            payloads    = split_and_prepare_payloads(
                message, num_parts, inner_key, outer_key, ctr_key
            )
            stego_paths = []
            for i, (enc_seq_id, enc_content) in enumerate(payloads):
                full_data = enc_seq_id + enc_content
                out_path  = str(stego_dir / f"stego_{i}.png")
                ok = embed_data(cover_paths[i], full_data, out_path)
                if ok:
                    stego_paths.append(out_path)
                else:
                    st.error(f"Stego embedding failed for image {i + 1}.")
                    return

        st.session_state.stego_paths  = stego_paths
        st.session_state.enc_sym_keys = enc_sym_keys
        st.session_state.send_stage   = "preview"
        st.rerun()

    except Exception as exc:
        st.error(f"Encryption pipeline error: {exc}")


def _send_preview(partner: str) -> None:
    """Show staged stego-images and wait for the sender to approve before delivery."""
    st.markdown(
        f'<div class="sc-alert sc-alert-info">'
        f'✓ Encryption complete. Review the stego-images below, then press <b>OK — SEND</b> '
        f'to deliver them to <b>{partner}</b>\'s inbox.'
        f'</div>',
        unsafe_allow_html=True,
    )

    stego_paths = st.session_state.stego_paths
    n_cols = min(len(stego_paths), 4)
    cols   = st.columns(n_cols)
    for i, path in enumerate(stego_paths):
        with cols[i % n_cols]:
            try:
                img = Image.open(path)
                buf = BytesIO()
                img.save(buf, format="PNG")
                st.image(buf.getvalue(), width="stretch")
                st.markdown(
                    f'<div class="sc-img-label">STEGO_{i + 1}.PNG</div>',
                    unsafe_allow_html=True,
                )
            except Exception:
                st.warning(f"Could not preview stego_{i}.png")

    st.markdown('<hr class="sc-divider">', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ OK — SEND TO INBOX", width="stretch", key="btn_ok_send"):
            _commit_to_inbox(partner)
    with c2:
        if st.button("✗ CANCEL", width="stretch", key="btn_cancel_send"):
            st.session_state.send_stage   = None
            st.session_state.stego_paths  = []
            st.session_state.enc_sym_keys = None
            st.rerun()


def _commit_to_inbox(partner: str) -> None:
    """Copy staged stego-images and the RSA-sealed key blob to partner's inbox."""
    inbox = INBOX_DIR / partner

    for f in inbox.iterdir():
        f.unlink(missing_ok=True)

    for src in st.session_state.stego_paths:
        shutil.copy2(src, inbox / Path(src).name)

    (inbox / "keys.bin").write_bytes(st.session_state.enc_sym_keys)

    st.session_state.send_stage   = "sent"
    st.session_state.stego_paths  = []
    st.session_state.enc_sym_keys = None
    st.rerun()
