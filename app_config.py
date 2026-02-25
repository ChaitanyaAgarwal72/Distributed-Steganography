from pathlib import Path

BASE_DIR         = Path(__file__).parent
DATA_DIR         = BASE_DIR / "data"
INBOX_DIR        = DATA_DIR / "inbox"
STAGING_DIR      = DATA_DIR / "staging"
PUBLIC_KEYS_FILE = DATA_DIR / "public_keys.json"

for _u in ("alice", "bob"):
    (INBOX_DIR / _u).mkdir(parents=True, exist_ok=True)
STAGING_DIR.mkdir(parents=True, exist_ok=True)

USERS: dict[str, str] = {
    "alice": "alice123",
    "bob":   "bob123",
}

PARTNER: dict[str, str] = {
    "alice": "bob",
    "bob":   "alice",
}

ENC_SEQ_ID_LEN: int = 12
