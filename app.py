import streamlit as st

from helpers.session import init_state
from ui.styles       import inject_css
from ui.login        import screen_login
from ui.dashboard    import screen_dashboard



def main() -> None:
    st.set_page_config(
        page_title="SecureChat · E2EE Stego",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    inject_css()
    init_state()

    if not st.session_state.logged_in:
        screen_login()
    else:
        screen_dashboard()


if __name__ == "__main__":
    main()

