import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

COVER_IMAGE_DIR = os.path.join(DATA_DIR, 'cover_img')
STEGO_IMAGE_DIR = os.path.join(DATA_DIR, 'stego_img')
OUTPUT_DIR = os.path.join(DATA_DIR, 'decrypted_output')

os.makedirs(COVER_IMAGE_DIR, exist_ok=True)
os.makedirs(STEGO_IMAGE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def _load_key_from_env(var_name: str, expected_len: int) -> bytes:
	value = os.getenv(var_name)
	if value is None:
		raise RuntimeError(
			f"Missing {var_name} in .env. Please set {var_name} to a {expected_len}-byte string."
		)

	key_bytes = value.encode("utf-8")
	if len(key_bytes) != expected_len:
		raise RuntimeError(
			f"Invalid {var_name} length: expected {expected_len} bytes, got {len(key_bytes)}. "
			"Tip: use exactly that many ASCII characters in .env."
		)
	return key_bytes


INNER_KEY = _load_key_from_env("INNER_KEY", 32)
OUTER_KEY = _load_key_from_env("OUTER_KEY", 16)
CTR_KEY = _load_key_from_env("CTR_KEY", 16)