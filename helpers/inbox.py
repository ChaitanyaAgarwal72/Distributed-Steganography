from app_config import INBOX_DIR


def inbox_has_message(username: str) -> bool:
    """Return True when a sender has deposited a sealed message."""
    return (INBOX_DIR / username / "keys.bin").exists()


def clear_inbox(username: str) -> None:
    """Delete all files from the user's inbox after they have read the message."""
    for f in (INBOX_DIR / username).iterdir():
        f.unlink(missing_ok=True)
