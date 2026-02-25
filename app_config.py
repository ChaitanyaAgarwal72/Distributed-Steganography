import streamlit as st
from pathlib import Path

BASE_DIR         = Path(__file__).parent
DATA_DIR         = BASE_DIR / "data"
INBOX_DIR        = DATA_DIR / "inbox"
STAGING_DIR      = DATA_DIR / "staging"
PUBLIC_KEYS_FILE = DATA_DIR / "public_keys.json"

USERS: dict[str, str] = dict(st.secrets["users"])

PARTNER: dict[str, str] = {
    u: next(v for v in USERS if v != u)
    for u in USERS
}

for _u in USERS:
    (INBOX_DIR / _u).mkdir(parents=True, exist_ok=True)
STAGING_DIR.mkdir(parents=True, exist_ok=True)

ENC_SEQ_ID_LEN: int = 12
