import streamlit as st

_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* ── Global ─────────────────────────────────────────────────────── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── App background ─────────────────────────────────────────────── */
.stApp {
    background: radial-gradient(ellipse at 20% 20%, #071220 0%, #060d19 60%, #040c16 100%);
}

/* ── Hide Streamlit chrome ───────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.2rem !important; max-width: 1400px; }

/* ── Top header bar ──────────────────────────────────────────────── */
.sc-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: linear-gradient(90deg, rgba(0,255,163,0.06) 0%, rgba(99,102,241,0.06) 100%);
    border: 1px solid rgba(0,255,163,0.12);
    border-radius: 14px;
    padding: 0.75rem 1.4rem;
    margin-bottom: 1.4rem;
}
.sc-brand {
    font-family: 'Space Mono', monospace;
    color: #00ffa3;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.06em;
}
.sc-user-badge {
    background: rgba(99,102,241,0.18);
    border: 1px solid rgba(99,102,241,0.35);
    color: #a5b4fc;
    padding: 0.25rem 0.85rem;
    border-radius: 20px;
    font-size: 0.78rem;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    letter-spacing: 0.08em;
}

/* ── Panel card ──────────────────────────────────────────────────── */
.sc-panel {
    background: rgba(10, 18, 35, 0.82);
    border: 1px solid rgba(148,163,184,0.08);
    border-radius: 16px;
    padding: 1.4rem;
    margin-bottom: 1rem;
}
.sc-panel-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(71,85,105,0.18);
}

/* ── Key status rows ─────────────────────────────────────────────── */
.sc-key-row {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    padding: 0.45rem 0.7rem;
    border-radius: 8px;
    margin-bottom: 0.45rem;
    background: rgba(15,23,42,0.5);
    font-size: 0.8rem;
}
.sc-dot-ok   { color: #00ffa3; font-size: 0.7rem; }
.sc-dot-warn { color: #f59e0b; font-size: 0.7rem; }
.sc-dot-err  { color: #ef4444; font-size: 0.7rem; }
.sc-key-label { color: #94a3b8; flex: 1; font-weight: 500; }
.sc-key-status-ok   { color: #00ffa3; font-size: 0.7rem; font-family: 'Space Mono', monospace; font-weight: 700; }
.sc-key-status-warn { color: #f59e0b; font-size: 0.7rem; font-family: 'Space Mono', monospace; font-weight: 700; }
.sc-key-status-err  { color: #ef4444; font-size: 0.7rem; font-family: 'Space Mono', monospace; font-weight: 700; }

/* ── Alert boxes ─────────────────────────────────────────────────── */
.sc-alert {
    padding: 0.7rem 1rem;
    border-radius: 10px;
    font-size: 0.82rem;
    margin: 0.5rem 0;
    font-weight: 500;
    line-height: 1.5;
}
.sc-alert-ok   { background: rgba(0,255,163,0.06);  border: 1px solid rgba(0,255,163,0.22);  color: #00ffa3; }
.sc-alert-warn { background: rgba(245,158,11,0.07); border: 1px solid rgba(245,158,11,0.25); color: #fbbf24; }
.sc-alert-info { background: rgba(99,102,241,0.07); border: 1px solid rgba(99,102,241,0.22); color: #a5b4fc; }
.sc-alert-err  { background: rgba(239,68,68,0.07);  border: 1px solid rgba(239,68,68,0.22);  color: #f87171; }

/* ── Revealed message ────────────────────────────────────────────── */
.sc-revealed {
    background: rgba(0,255,163,0.04);
    border: 1px solid rgba(0,255,163,0.28);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    color: #00ffa3;
    word-break: break-word;
    white-space: pre-wrap;
    margin: 0.8rem 0;
    line-height: 1.7;
}

/* ── Section divider ─────────────────────────────────────────────── */
.sc-divider {
    border: none;
    border-top: 1px solid rgba(71,85,105,0.15);
    margin: 1rem 0;
}

/* ── Image frame ─────────────────────────────────────────────────── */
.sc-img-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #475569;
    text-align: center;
    letter-spacing: 0.08em;
    margin-top: 0.3rem;
}

/* ── Streamlit buttons reskin ────────────────────────────────────── */
div.stButton > button {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.74rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.06em !important;
    border-radius: 9px !important;
    border: 1px solid rgba(99,102,241,0.35) !important;
    background: rgba(99,102,241,0.1) !important;
    color: #a5b4fc !important;
    transition: all 0.18s ease !important;
    padding: 0.5rem 1rem !important;
}
div.stButton > button:hover {
    background: rgba(99,102,241,0.22) !important;
    border-color: rgba(99,102,241,0.6) !important;
    color: #e0e7ff !important;
}
div.stButton > button:focus,
div.stButton > button:active {
    background: rgba(99,102,241,0.3) !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.4) !important;
}

/* ── Streamlit form submit (accent variant) ──────────────────────── */
div.stFormSubmitButton > button {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    border-radius: 9px !important;
    border: 1px solid rgba(0,255,163,0.4) !important;
    background: rgba(0,255,163,0.1) !important;
    color: #00ffa3 !important;
    transition: all 0.18s ease !important;
}
div.stFormSubmitButton > button:hover {
    background: rgba(0,255,163,0.2) !important;
    border-color: rgba(0,255,163,0.7) !important;
}

/* ── Login container ─────────────────────────────────────────────── */
.sc-login-wrap {
    max-width: 420px;
    margin: 4vh auto 0;
    padding: 2.5rem 2rem;
    background: rgba(10,18,35,0.9);
    border: 1px solid rgba(0,255,163,0.12);
    border-radius: 20px;
    box-shadow: 0 8px 40px rgba(0,255,163,0.04), 0 2px 16px rgba(0,0,0,0.5);
}

/* ── Input overrides ─────────────────────────────────────────────── */
.stTextArea textarea, .stTextInput input {
    background: rgba(10,18,35,0.7) !important;
    border-color: rgba(71,85,105,0.4) !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: rgba(99,102,241,0.6) !important;
    box-shadow: 0 0 0 1px rgba(99,102,241,0.4) !important;
}

/* ── Column card panels ──────────────────────────────────────────── */
[data-testid="stVerticalBlock"] > [data-testid="stVerticalBlock"] {
    border-radius: 14px;
}

/* ── Progress / spinner ──────────────────────────────────────────── */
.stSpinner > div { border-top-color: #00ffa3 !important; }
</style>
"""


def inject_css() -> None:
    """Inject the full dark-cyber theme stylesheet into the Streamlit app."""
    st.markdown(_CSS, unsafe_allow_html=True)
