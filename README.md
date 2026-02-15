## Distributed Steganography

Hide messages across multiple images using layered encryption (ChaCha20 + ASCON + AES-CTR) and LSB steganography.

### Features
- Split secret text into N chunks, encrypt twice, shuffle, and embed into separate images.
- Extract stego images, verify integrity, decrypt, and reassemble in order.
- Minimal CLI flow: choose hide or reveal; user supplies chunk count at runtime.

### Requirements
- Python 3.10+
- Dependencies: ascon, numpy, pillow, pycryptodome, python-dotenv

### Setup
1) Install deps:
```
pip install -r requirements.txt
```
2) Create `.env` in project root with keys (ASCII, exact lengths):
```
INNER_KEY=32charsforchacha20keyexact!
OUTER_KEY=16charsforascon!
CTR_KEY=16charsforaesctr!
```
3) Place cover images in `data/cover_img/` (PNG/JPG). Ensure at least as many images as chunks you will request.

### Usage
Run the CLI:
```
python main.py
```
- Option 1 (Hide):
	- Enter secret message.
	- Enter number of images to use (must be <= available cover images).
	- Stego outputs saved to `data/stego_img/stego_<index>.png`.
- Option 2 (Reveal):
	- Reads `data/stego_img/stego_*.png`, decrypts, and writes `data/decrypted_output/secret.txt`.

### How it works (brief)
- Split message into N parts.
- Encrypt each chunk with ChaCha20, wrap with ASCON-128 for integrity, encrypt sequence ID with AES-CTR, shuffle bundles.
- Embed bytes into image LSBs with a length header; extraction reverses the process and sorts by decrypted IDs.

### Project structure
- `main.py` – CLI orchestrator.
- `src/crypto/` – AES-CTR, ChaCha20, ASCON helpers.
- `src/utils/chunk_manager.py` – splitting, shuffling, and reassembly logic.
- `src/stego/lsb_engine.py` – LSB embed/extract.
- `data/` – cover inputs, stego outputs, decrypted output file.

### Notes
- Keys must match required lengths or loading will fail.
- Cover images must be large enough to store the payload; the tool reports if too small.
