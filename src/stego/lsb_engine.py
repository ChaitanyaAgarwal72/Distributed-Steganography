from PIL import Image
import numpy as np
import os

def msg_to_bin(msg):
    """Converts a string or bytes to a binary string."""
    if type(msg) == str:
        return ''.join([format(ord(i), "08b") for i in msg])
    elif type(msg) == bytes:
        return ''.join([format(i, "08b") for i in msg])
    elif type(msg) == np.ndarray or type(msg) == int:
        return format(msg, "08b")
    else:
        raise TypeError("Input type not supported")

def bin_to_bytes(binary_str):
    """Converts a binary string back to bytes."""
    return int(binary_str, 2).to_bytes((len(binary_str) + 7) // 8, byteorder='big')

def embed_data(image_path, secret_data, output_path):
    """
    Embeds binary data into the LSB of an image.
    Args:
        image_path (str): Path to cover image.
        secret_data (bytes): The encrypted chunk to hide.
        output_path (str): Where to save the stego-image.
    """
    try:
        image = Image.open(image_path).convert('RGB')
        pixels = np.array(image)
    except Exception as e:
        print(f"Error opening image {image_path}: {e}")
        return False

    data_len = len(secret_data)
    bin_len = format(data_len, '032b')
    bin_data = bin_len + msg_to_bin(secret_data)

    total_pixels = pixels.size // 3
    req_pixels = len(bin_data)
    
    if req_pixels > total_pixels:
        print(f"ERROR: Image {image_path} is too small! Need {req_pixels} bits, have {total_pixels}.")
        return False

    print(f"[STEGO] Hiding {len(secret_data)} bytes in {os.path.basename(image_path)}...")

    flat_pixels = pixels.flatten()

    for i in range(req_pixels):
        val = flat_pixels[i]
        bit = int(bin_data[i])
        if bit == 0:
            flat_pixels[i] = val & 254
        else:
            flat_pixels[i] = val | 1
    new_pixels = flat_pixels.reshape(pixels.shape)
    new_image = Image.fromarray(new_pixels.astype('uint8'), 'RGB')
    new_image.save(output_path)
    return True

def extract_data(stego_image_path):
    """
    Extracts binary data from the LSB of an image.
    Returns:
        bytes: The extracted secret data.
    """
    try:
        image = Image.open(stego_image_path).convert('RGB')
        pixels = np.array(image).flatten()
    except Exception as e:
        print(f"Error opening image {stego_image_path}: {e}")
        return None

    len_bits = ""
    for i in range(32):
        len_bits += str(pixels[i] & 1)
        
    data_len = int(len_bits, 2)

    total_bits = data_len * 8
    data_bits = ""

    for i in range(32, 32 + total_bits):
        data_bits += str(pixels[i] & 1)

    return bin_to_bytes(data_bits)