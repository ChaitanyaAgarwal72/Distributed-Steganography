import random
import struct

from src.crypto.aes_cipher import encrypt_aes, decrypt_aes
from src.crypto.chacha_cipher import encrypt_chacha, decrypt_chacha
from src.crypto.ascon_cipher import encrypt_ascon, decrypt_ascon

def split_and_prepare_payloads(message, num_parts, inner_key, outer_key, ctr_key):
    """
    Splits message and applies Tri-Hybrid Encryption:
    1. Content: ChaCha20 (Inner) -> ASCON-128 (Outer)
    2. Sequence ID: AES-128 (CTR Mode)
    """
    n = len(message)
    k = num_parts
    chunk_size = (n + k - 1) // k
    chunks = [message[i:i + chunk_size] for i in range(0, n, chunk_size)]
    while len(chunks) < num_parts:
        chunks.append("") 

    payloads = []
    print(f"[DEBUG] Processing {len(chunks)} chunks with TRI-HYBRID Encryption...")

    for seq_id, chunk_text in enumerate(chunks):
        inner_data = encrypt_chacha(chunk_text, inner_key)
        double_enc_content = encrypt_ascon(inner_data, outer_key)
        seq_bytes = struct.pack('>I', seq_id)
        enc_seq_id = encrypt_aes(seq_bytes, ctr_key)
        payloads.append((enc_seq_id, double_enc_content))
    random.shuffle(payloads)
    return payloads

def reassemble_payloads(shuffled_payloads, inner_key, outer_key, ctr_key):
    """
    Decrypts AES IDs to sort, then unwraps ASCON -> ChaCha content.
    """
    decrypted_parts = []
    print(f"[DEBUG] Reassembling {len(shuffled_payloads)} chunks...")

    for enc_seq_id, double_enc_content in shuffled_payloads:
        seq_bytes = decrypt_aes(enc_seq_id, ctr_key)
        if seq_bytes is None:
            raise ValueError("TAMPER ALERT: Sequence ID corrupted!")
        seq_id = struct.unpack('>I', seq_bytes)[0]
        inner_data = decrypt_ascon(double_enc_content, outer_key)
        if inner_data is None:
            raise ValueError(f"TAMPER ALERT: ASCON Layer failed for chunk {seq_id}.")
        chunk_text = decrypt_chacha(inner_data, inner_key)
        if chunk_text is None:
            raise ValueError(f"ERROR: ChaCha Layer failed for chunk {seq_id}.")
        decrypted_parts.append((seq_id, chunk_text))
        
    decrypted_parts.sort(key=lambda x: x[0])
    return "".join(part[1] for part in decrypted_parts)