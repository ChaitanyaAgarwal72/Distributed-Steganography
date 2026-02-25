import streamlit as st

from helpers.rsa_utils import load_public_keys, generate_rsa_keypair, save_public_key


def panel_key_status(user: str, partner: str) -> None:
    st.markdown('<div class="sc-panel">', unsafe_allow_html=True)
    st.markdown('<div class="sc-panel-title">🔑 Key Status</div>', unsafe_allow_html=True)

    keys_gen      = st.session_state.keys_generated
    public_keys   = load_public_keys()
    partner_ready = partner in public_keys

    if keys_gen:
        st.markdown(
            '<div class="sc-key-row">'
            '<span class="sc-dot-ok">●</span>'
            '<span class="sc-key-label">Your RSA-2048</span>'
            '<span class="sc-key-status-ok">ACTIVE</span>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="sc-key-row">'
            '<span class="sc-dot-err">●</span>'
            '<span class="sc-key-label">Your RSA-2048</span>'
            '<span class="sc-key-status-err">NONE</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    if partner_ready:
        st.markdown(
            f'<div class="sc-key-row">'
            f'<span class="sc-dot-ok">●</span>'
            f'<span class="sc-key-label">{partner.capitalize()} pubkey</span>'
            f'<span class="sc-key-status-ok">READY</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="sc-key-row">'
            f'<span class="sc-dot-warn">●</span>'
            f'<span class="sc-key-label">{partner.capitalize()} pubkey</span>'
            f'<span class="sc-key-status-warn">WAITING</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="sc-divider">', unsafe_allow_html=True)

    if not keys_gen:
        if st.button("⚡ GENERATE RSA KEYS", width="stretch", key="btn_gen_keys"):
            with st.spinner("Generating RSA-2048 keypair…"):
                priv, pub_pem = generate_rsa_keypair()
                st.session_state.private_key    = priv
                st.session_state.keys_generated = True
                save_public_key(user, pub_pem)
            st.success("Keys generated & published.")
            st.rerun()
    else:
        st.markdown(
            '<div style="font-size:.7rem;color:#1e293b;font-family:Space Mono,monospace;'
            'line-height:1.6;padding:0.5rem;background:rgba(0,0,0,.3);border-radius:8px;">'
            '🔒 Private key secured<br>in session memory.<br><br>'
            '☁ Public key published<br>to relay registry.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sc-panel">', unsafe_allow_html=True)
    st.markdown('<div class="sc-panel-title">⚙ Crypto Pipeline</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="font-size:.7rem;color:#475569;font-family:'Space Mono',monospace;line-height:2;">
          <span style="color:#6366f1;">L1</span> ChaCha20<br>
          <span style="color:#6366f1;">↓</span><br>
          <span style="color:#8b5cf6;">L2</span> ASCON-128<br>
          <span style="color:#8b5cf6;">↓</span><br>
          <span style="color:#a855f7;">L3</span> AES-128-CTR<br>
          <span style="color:#a855f7;">&nbsp;&nbsp;</span>(seq IDs)<br>
          <span style="color:#a855f7;">↓</span><br>
          <span style="color:#00ffa3;">★</span> LSB Stego<br>
          <span style="color:#00ffa3;">↓</span><br>
          <span style="color:#f59e0b;">⬡</span> RSA-2048 KEM
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)
