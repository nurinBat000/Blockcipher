## block cipher specialist :3
## Nurin Batrisyia here! (AM2512021847)
## implementation + performance benchmarking included // 8-round custom Feistel block cipher

import time
import os

def round_function(r_half, round_key):
    combined = (r_half + round_key) & 0xFF
    return (combined ^ (r_half >> 2)) & 0xFF

def generate_subkeys(master_key):
    keys = []
    for i in range(8):
        derived_key = (master_key * (i + 3) + 13) % 256
        keys.append(derived_key)
    return keys

def feistel_cipher_core(left_byte, right_byte, subkeys, mode='encrypt'):
    current_left = left_byte
    current_right = right_byte

    for i in range(8):
        if mode == 'encrypt':
            rk = subkeys[i]
        else:
            rk = subkeys[7 - i]

        next_left = current_right
        next_right = current_left ^ round_function(current_right, rk)

        current_left = next_left
        current_right = next_right

        return current_left, current_right

def run_cryptography_on_file(input_path, output_path, subkeys, mode='encrypt'):
    processed_data = bytearray()

    with open(input_path, 'rb') as source_file:
        raw_bytes = source_file.read()
    index = 0

    while index < len(raw_bytes):
        if index + 1 < len(raw_bytes):
            l_byte = raw_bytes[index]
            r_byte = raw_bytes[index + 1]
        else:
            l_byte = raw_bytes[index]
            r_byte = 0 

        new_l, new_r = feistel_cipher_core(l_byte, r_byte, subkeys, mode)
        processed_data.append(new_l)
        processed_data.append(new_r)

        index += 2

    with open(output_path, 'wb') as target_file:
        target_file.write(processed_data)

if __name__ == "__main__":
    MASTER_KEY = 88  
    subkey_list = generate_subkeys(MASTER_KEY)

    print("==BLOCK CIPHER SPECIALIST SYSTEM=")
    print(f"Master Key: {MASTER_KEY}")
    print(f"Generated 8 Subkeys: {subkey_list}\n")
    print("Starting encryption & decryption benchmarks using team files...")
    print("-" * 65)

    team_files = [
        "1kb-testfile.txt",
        "100kb-testfile.txt",
        "1mb-testfile.txt"
    ]

    for file_name in team_files:
        if not os.path.exists(file_name):
            print(f"Error: File [{file_name}] not found! Check your folder layout.")
            continue

        encrypted_output = f"encrypted_{file_name}.enc"
        decrypted_output = f"decrypted_{file_name}"

        start_enc = time.time()
        run_cryptography_on_file(file_name, encrypted_output, subkey_list, mode='encrypt')
        end_enc = time.time()
        encryption_time = (end_enc - start_enc) * 1000  

        start_dec = time.time()
        run_cryptography_on_file(encrypted_output, decrypted_output, subkey_list, mode='decrypt')
        end_dec = time.time()
        decryption_time = (end_dec - start_dec) * 1000  

        print(f"File: {file_name}")
        print(f"  > Encryption Time : {encryption_time:.2f} ms")
        print(f"  > Decryption Time : {decryption_time:.2f} ms")
        print("-" * 65)

        try:
            os.remove(encrypted_output)
            os.remove(decrypted_output)
        except OSError:
            pass

    print("Benchmark complete!")
