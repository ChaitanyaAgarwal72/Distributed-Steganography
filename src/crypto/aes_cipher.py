from Crypto.Cipher import AES
from Crypto.Util import Counter
import os

def encrypt_aes(plaintext, key):
    """
    Encrypts data using AES-128 in CTR mode.
    Args:
        plaintext (bytes): The data to encrypt (e.g., Sequence ID).
        key (bytes): Must be 16, 24, or 32 bytes.
    Returns:
        bytes: nonce(8) + ciphertext
    """
    nonce = os.urandom(8)
    ctr = Counter.new(64, prefix=nonce)
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    ciphertext = cipher.encrypt(plaintext)
    return nonce + ciphertext

def decrypt_aes(encrypted_data, key):
    """
    Decrypts AES-CTR data.
    """
    try:
        nonce = encrypted_data[:8]
        ciphertext = encrypted_data[8:]
        ctr = Counter.new(64, prefix=nonce)
        cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext
        
    except Exception as e:
        print(f"AES Decryption Error: {e}")
        return None