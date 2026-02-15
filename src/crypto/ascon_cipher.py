import ascon
import os

def encrypt_ascon(data_bytes, key):
    """
    Encrypts bytes using ASCON-128 (Authenticated Encryption).
    Args:
        data_bytes (bytes): Data to encrypt (e.g., Sequence ID or ChaCha output).
        key (bytes): 16-byte key.
    Returns:
        bytes: nonce(16) + ciphertext + tag(16)
    """
    nonce = os.urandom(16)
    ciphertext = ascon.encrypt(
        key, 
        nonce, 
        associateddata=b"", 
        plaintext=data_bytes, 
        variant="Ascon-128"
    )
    return nonce + ciphertext

def decrypt_ascon(encrypted_payload, key):
    """
    Decrypts and Verifies ASCON-128 data.
    Args:
        encrypted_payload (bytes): nonce(16) + ciphertext + tag.
        key (bytes): 16-byte key.
    Returns:
        bytes: The decrypted data, or None if integrity check fails.
    """
    try:
        nonce = encrypted_payload[:16]
        ciphertext_with_tag = encrypted_payload[16:]
        plaintext = ascon.decrypt(
            key, 
            nonce, 
            associateddata=b"", 
            ciphertext=ciphertext_with_tag, 
            variant="Ascon-128"
        )
        return plaintext
        
    except ValueError:
        print("CRITICAL SECURITY ALERT: ASCON Integrity Check Failed! Data was tampered.")
        return None
    except Exception as e:
        print(f"ASCON Error: {e}")
        return None