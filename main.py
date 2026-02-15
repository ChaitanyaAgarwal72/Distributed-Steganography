import os
import glob
from src.utils.chunk_manager import split_and_prepare_payloads, reassemble_payloads
from src.stego.lsb_engine import embed_data, extract_data
import config

def main():
    print("=== StegoASCON Distributed System ===")
    print("1. Hide Message (Distribute)")
    print("2. Reveal Message (Reassemble)")
    choice = input("Select Option (1/2): ")

    if choice == '1':
        secret_msg = input("Enter Secret Message: ")
        try:
            num_parts = int(input("Enter number of images to use: "))
        except ValueError:
            print("Invalid number entered.")
            return
        if num_parts <= 0:
            print("Number of images must be positive.")
            return
        
        images = glob.glob(os.path.join(config.COVER_IMAGE_DIR, "*.*"))
        
        if len(images) < num_parts:
            print(f"ERROR: Not enough images! Need {num_parts}, found {len(images)}.")
            return

        payloads = split_and_prepare_payloads(
            secret_msg, 
            num_parts, 
            config.INNER_KEY, 
            config.OUTER_KEY,
            config.CTR_KEY
        )

        for i, (payload_bundle) in enumerate(payloads):
            enc_seq_id, enc_content = payload_bundle
            full_data = enc_seq_id + enc_content
            cover_img = images[i]
            output_name = f"stego_{i}.png"
            output_path = os.path.join(config.STEGO_IMAGE_DIR, output_name)
            
            success = embed_data(cover_img, full_data, output_path)
            if success:
                print(f"Saved: {output_name}")

        print(f"\nDistribution Complete! Sent {num_parts} randomized parts.")

    elif choice == '2':
        print("Scanning stego_images folder...")
        stego_files = glob.glob(os.path.join(config.STEGO_IMAGE_DIR, "stego_*.png"))
        
        if not stego_files:
            print("No stego images found!")
            return

        recovered_payloads = []

        for img_path in stego_files:
            raw_data = extract_data(img_path)
            
            if raw_data:
                enc_seq_id = raw_data[:12]
                enc_content = raw_data[12:]
                
                recovered_payloads.append((enc_seq_id, enc_content))

        try:
            message = reassemble_payloads(
                recovered_payloads, 
                config.INNER_KEY, 
                config.OUTER_KEY,
                config.CTR_KEY
            )
            print("\n-----------------------------")
            print(f"SUCCESS! Decrypted Message: {message}")
            print("-----------------------------")
            with open(os.path.join(config.OUTPUT_DIR, "secret.txt"), "w") as f:
                f.write(message)
                
        except Exception as e:
            print(f"FAILED: {e}")

if __name__ == "__main__":
    main()