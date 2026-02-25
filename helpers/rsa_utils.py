import json

from Crypto.PublicKey import RSA
from Crypto.Cipher   import PKCS1_OAEP

from app_config import PUBLIC_KEYS_FILE

def load_public_keys() -> dict[str, str]:
    """Return {username: PEM string} from the shared registry file."""
    if PUBLIC_KEYS_FILE.exists():
        return json.loads(PUBLIC_KEYS_FILE.read_text())
    return {}


def save_public_key(username: str, pem: str) -> None:
    """Publish a user's public key to the shared registry."""
    keys = load_public_keys()
    keys[username] = pem
    PUBLIC_KEYS_FILE.write_text(json.dumps(keys, indent=2))

def generate_rsa_keypair() -> tuple:
    """
    Generate a fresh RSA-2048 keypair.
    Returns:
        (private_key_obj, public_pem_str)
    The private key object stays in st.session_state and never leaves the client.
    """
    key = RSA.generate(2048)
    return key, key.publickey().export_key().decode()

def rsa_encrypt_sym_keys(
    inner: bytes,
    outer: bytes,
    ctr:   bytes,
    pub_pem: str,
) -> bytes:
    """
    Pack the 3 symmetric keys into a 64-byte blob and RSA-OAEP-encrypt it
    with the recipient's public key.

    Layout: inner_key(32) + outer_key(16) + ctr_key(16) = 64 bytes
    """
    blob = inner + outer + ctr
    return PKCS1_OAEP.new(RSA.import_key(pub_pem)).encrypt(blob)


def rsa_decrypt_sym_keys(
    enc_blob: bytes,
    priv_key,
) -> tuple[bytes, bytes, bytes]:
    """
    RSA-OAEP-decrypt the key blob and unpack the 3 symmetric keys.

    Returns:
        (inner_key, outer_key, ctr_key)
    """
    blob = PKCS1_OAEP.new(priv_key).decrypt(enc_blob)
    return blob[0:32], blob[32:48], blob[48:64]
