import streamlit as st

from app_config import USERS


def screen_login() -> None:
    _, col, _ = st.columns([1, 1.5, 1])
    with col:
        st.markdown(
            """
            <div class="sc-login-wrap">
              <div style="text-align:center;margin-bottom:1.8rem;">
                <div style="font-size:3rem;margin-bottom:.6rem;filter:drop-shadow(0 0 14px #00ffa3aa);">🔐</div>
                <div style="font-family:'Space Mono',monospace;color:#00ffa3;font-size:1.55rem;font-weight:700;letter-spacing:.04em;">SecureChat</div>
                <div style="font-family:'Space Mono',monospace;color:#334155;font-size:.7rem;letter-spacing:.14em;margin-top:.3rem;">
                  E2EE · TRI-HYBRID CRYPTO · LSB STEGO
                </div>
              </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("login_form", clear_on_submit=False):
            username = st.selectbox(
                "Select user",
                list(USERS.keys()),
                format_func=str.capitalize,
                key="sel_user",
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter password…",
                key="inp_pass",
            )
            submitted = st.form_submit_button("SIGN IN →", width="stretch")

        if submitted:
            if USERS.get(username) == password:
                st.session_state.logged_in = True
                st.session_state.username  = username
                st.rerun()
            else:
                st.markdown(
                    '<div class="sc-alert sc-alert-err" style="text-align:center;">✗ Invalid credentials</div>',
                    unsafe_allow_html=True,
                )

        st.markdown(
            """<div style="text-align:center;color:#334155;font-size:.7rem;
                          margin-top:1.2rem;font-family:'Space Mono',monospace;">
               alice / alice123 &nbsp;·&nbsp; bob / bob123
               </div></div>""",
            unsafe_allow_html=True,
        )
