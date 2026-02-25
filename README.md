## Distributed Steganography with Multi-Layer Cryptography

A Network and Information Security project that demonstrates secure covert data transmission by distributing encrypted message chunks across multiple images using layered cryptography and LSB steganography.

The core system splits a secret payload into N chunks, encrypts each through a tri-hybrid cipher pipeline, encapsulates the symmetric keys with RSA-2048, shuffles the chunks, and embeds them into separate PNG cover images. Extraction reverses the process: decapsulate keys, pull payloads from images, sort by decrypted sequence IDs, and reassemble the original message.

A **Streamlit web UI is included as a demo front-end** to interact with the system visually. The underlying engine (`src/`) is fully independent of it.

---

### Features
- **Tri-hybrid encryption**: ChaCha20 (confidentiality) → ASCON-128 (integrity/authentication) → AES-128-CTR (sequence-ID obfuscation).
- **RSA-2048 KEM** — per-run random symmetric keys wrapped with the recipient's RSA public key; no pre-shared secrets.
- **LSB steganography** — encrypted payload embedded into PNG cover images; stego images are visually identical to originals.
- **Distributed chunking** — message split across N images and shuffled; order recovered at extraction via encrypted sequence IDs.
- **Integrity protection** — ASCON-128 authentication tag ensures tampered chunks are detected and rejected.
- **Demo UI** — Streamlit front-end for visualising the full pipeline end-to-end between two parties.

---

### Crypto Pipeline

```
Plaintext
   │
   ▼  ChaCha20  (32-byte key)   ← confidentiality
   │
   ▼  ASCON-128 (16-byte key)   ← integrity + authentication
   │
   ▼  AES-128-CTR (16-byte key) ← sequence-ID obfuscation
   │
   ▼  RSA-2048 OAEP             ← key encapsulation (KEM)
   │
   ▼  LSB Embed → stego PNG(s)
```

---

### Requirements
- Python 3.10+
- Dependencies: `ascon`, `numpy`, `pillow`, `pycryptodome`, `streamlit`

---

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. *(Optional)* Launch the demo UI:
```bash
streamlit run app.py
```
Then open `http://localhost:8501` in your browser.

> No `.env` file or pre-shared secrets needed — all symmetric keys are generated randomly per run via `get_random_bytes`.

---

### How It Works

#### Embed (Sender side)
1. Secret message is split into N equal chunks.
2. Each chunk is encrypted through the tri-hybrid pipeline (ChaCha20 → ASCON-128 → AES-128-CTR).
3. An encrypted sequence ID is prepended to each chunk payload so order can be recovered after shuffling.
4. All symmetric keys (32 + 16 + 16 = 64 bytes) are RSA-OAEP encrypted with the recipient's public key and stored alongside the stego images.
5. Payloads are shuffled and each is embedded into a separate PNG cover image via LSB encoding with a length header.

#### Extract (Receiver side)
1. Receiver decapsulates the 64-byte key blob using their RSA private key, recovering all three symmetric keys.
2. Raw bytes are extracted from each stego image (length-header guided).
3. The AES-CTR encrypted sequence ID (`first 12 bytes`) is decrypted to recover the original order.
4. Chunks are sorted by sequence ID, ASCON tag is verified, ChaCha20 is decrypted, and chunks are reassembled.

---

### Demo UI Usage

The Streamlit UI demonstrates the full pipeline interactively between two parties (User 1 and User 2):

1. **Login** — select a user (`user1` or `user2`) and enter the password.
2. **Generate RSA Keys** — create an RSA-2048 keypair and register the public key.
3. **Embed** — upload PNG cover images, type a secret message, encrypt & embed, then deliver to the recipient's inbox.
4. **Extract** — on the receiver side, check the inbox and decrypt to reveal the original message.

---

### Project Structure

```
app.py                  # Streamlit entry point
app_config.py           # Constants, paths, user table, directory bootstrap
helpers/
  rsa_utils.py          # RSA keypair generation, KEM wrap/unwrap, key registry I/O
  inbox.py              # Inbox filesystem helpers (check/clear per-user inbox)
  session.py            # st.session_state initialisation
ui/
  styles.py             # Dark-cyber CSS theme
  login.py              # Login screen
  dashboard.py          # Main dashboard layout
  panels/
    key_status.py       # Key Status panel + crypto pipeline legend
    send.py             # Send Message panel (encrypt + embed)
    receive.py          # Receive Message panel (extract + decrypt)
src/
  crypto/
    chacha_cipher.py    # ChaCha20 encrypt/decrypt
    ascon_cipher.py     # ASCON-128 encrypt/decrypt
    aes_cipher.py       # AES-128-CTR encrypt/decrypt
  stego/
    lsb_engine.py       # LSB embed/extract
  utils/
    chunk_manager.py    # Message splitting, shuffling, and reassembly
    img_loager.py       # Image loading helper
data/
  inbox/                # Per-user message queues (user1/, user2/)
  staging/              # Temporary workspace for encrypt/decrypt operations
  public_keys.json      # RSA public key registry (runtime-generated)
```

---

### Demo Users

| Username | Password  |
|----------|-----------|
| user1    | test111   |
| user2    | test222   |

---

### Notes
- Cover images must be large enough to embed the payload; the engine reports an error if capacity is exceeded.
- All runtime data (`data/inbox/`, `data/staging/`, `data/public_keys.json`) is excluded from version control via `.gitignore`.
