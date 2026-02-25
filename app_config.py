from pathlib import Path

BASE_DIR         = Path(__file__).parent
DATA_DIR         = BASE_DIR / "data"
INBOX_DIR        = DATA_DIR / "inbox"
STAGING_DIR      = DATA_DIR / "staging"
PUBLIC_KEYS_FILE = DATA_DIR / "public_keys.json"

for _u in ("user1", "user2"):
    (INBOX_DIR / _u).mkdir(parents=True, exist_ok=True)
STAGING_DIR.mkdir(parents=True, exist_ok=True)

USERS: dict[str, str] = {
    "user1": "test111",
    "user2": "test222",
}

PARTNER: dict[str, str] = {
    "user1": "user2",
    "user2": "user1",
}

ENC_SEQ_ID_LEN: int = 12
