## Secure E2EE Steganography Chat

A Network and Information Security project implementing end-to-end encrypted steganographic messaging between two users via a Streamlit web UI.

Messages are split into chunks, encrypted through a tri-hybrid cipher pipeline, encapsulated with RSA-2048, and embedded into PNG images using LSB steganography — making the communication both confidential and visually covert.

---

### Features
- **Streamlit web UI** — browser-based chat interface, no CLI required.
- **Tri-hybrid encryption**: ChaCha20 (confidentiality) → ASCON-128 (integrity/authentication) → AES-128-CTR (sequence-ID obfuscation).
- **RSA-2048 KEM** — per-message random symmetric keys wrapped with the recipient's RSA public key.
- **LSB steganography** — encrypted payload embedded into PNG cover images; stego images are indistinguishable from originals.
- **Chunked messaging** — message split across N images, shuffled, reassembled in order on the receiver side.
- **Per-session key generation** — no hardcoded secrets; keys are generated fresh at login.

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

2. Launch the app:
```bash
streamlit run app.py
```

3. Open the browser at `http://localhost:8501`.

> No `.env` file or pre-shared keys needed — all symmetric keys are generated randomly per message.

---

### Usage

1. **Login** — select a user (`alice` or `bob`) and enter the password.
2. **Generate RSA Keys** — click *Generate & Register Keys* in the Key Status panel to create your RSA-2048 keypair and publish your public key.
3. **Send a Message**:
   - Upload one or more PNG cover images.
   - Type your secret message and click *Encrypt & Embed*.
   - Preview the stego images, then click *Deliver to Inbox*.
4. **Receive a Message**:
   - Switch to the other user's session.
   - Click *Check Inbox* → *Decrypt & Reveal* to extract and display the original message.

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
  inbox/                # Per-user message queues (alice/, bob/)
  staging/              # Temporary workspace for encrypt/decrypt operations
  public_keys.json      # RSA public key registry (runtime-generated)
```

---

### Users (Demo)

| Username | Password  |
|----------|-----------|
| alice    | alice123  |
| bob      | bob123    |

---

### Notes
- Cover images must be large enough to embed the payload; the engine reports an error if capacity is exceeded.
- All runtime data (`data/inbox/`, `data/staging/`, `data/public_keys.json`) is excluded from version control via `.gitignore`.
