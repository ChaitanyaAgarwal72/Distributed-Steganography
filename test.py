from src.utils.chunk_manager import split_and_prepare_payloads, reassemble_payloads
import os

inner_key = os.urandom(32)
outer_key = os.urandom(16)
ctr_key = os.urandom(16)
num_parts = 5

message = "This is a very long top secret message that will be split into 5 parts."

payloads = split_and_prepare_payloads(message, num_parts, inner_key, outer_key, ctr_key)

print(f"Generated {len(payloads)} encrypted payloads.")
print("First payload sample (Enc_ID, Enc_Content):", payloads[0])

try:
    recovered = reassemble_payloads(payloads, inner_key, outer_key, ctr_key)
    print(f"\nOriginal:  {message}")
    print(f"Recovered: {recovered}")
    if message == recovered:
        print("\nSUCCESS: Logic is perfect!")
    else:
        print("\nFAIL: Mismatch.")
except Exception as e:
    print(f"ERROR: {e}")