from Crypto.Cipher import ChaCha20

def encrypt_chacha(plaintext, key):
    """
    Encrypts text using ChaCha20 Stream Cipher.
    Args:
        plaintext (str): The secret message.
        key (bytes): 32-byte key.
    Returns:
        bytes: nonce(8) + ciphertext
    """
    cipher = ChaCha20.new(key=key)
    data_bytes = plaintext.encode('utf-8')
    ciphertext = cipher.encrypt(data_bytes)
    return cipher.nonce + ciphertext

def decrypt_chacha(encrypted_data, key):
    """
    Decrypts ChaCha20 data.
    Args:
        encrypted_data (bytes): nonce(8) + ciphertext.
        key (bytes): 32-byte key.
    Returns:
        str: The original plaintext.
    """
    try:
        nonce = encrypted_data[:8]
        ciphertext = encrypted_data[8:]
        cipher = ChaCha20.new(key=key, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext.decode('utf-8')
        
    except (ValueError, KeyError) as e:
        print(f"ChaCha Decryption Error: {e}")
        return None