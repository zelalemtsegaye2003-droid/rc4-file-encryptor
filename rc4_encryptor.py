#!/usr/bin/env python3
"""
RC4 File Encryptor
Reads file.txt in binary mode, encrypts it with RC4, and writes the ciphertext back.
"""

import sys

def rc4_ksa(key: bytes) -> list:
    """Key Scheduling Algorithm — initializes the S permutation array."""
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) & 0xFF
        S[i], S[j] = S[j], S[i]
    return S

def rc4_prga(S: list, data_len: int) -> bytes:
    """Pseudo-Random Generation Algorithm — produces the keystream."""
    S = S[:]  # work on a copy
    i = j = 0
    keystream = bytearray()
    for _ in range(data_len):
        i = (i + 1) & 0xFF
        j = (j + S[i]) & 0xFF
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) & 0xFF]
        keystream.append(K)
    return bytes(keystream)

def rc4_encrypt(key: bytes, plaintext: bytes) -> bytes:
    """Encrypt (or decrypt) data using RC4."""
    S = rc4_ksa(key)
    keystream = rc4_prga(S, len(plaintext))
    return bytes(p ^ k for p, k in zip(plaintext, keystream))

def main():
    KEY = b"p4ssw0rd"  # Change this to your desired key
    
    filename = "file.txt"
    try:
        with open(filename, "rb") as f:
            plaintext = f.read()
    except FileNotFoundError:
        print(f"[-] Error: {filename} not found in the current directory.")
        sys.exit(1)
    
    print(f"[+] Read {len(plaintext)} bytes from {filename}")
    
    ciphertext = rc4_encrypt(KEY, plaintext)
    
    with open(filename, "wb") as f:
        f.write(ciphertext)
    
    print(f"[+] Encrypted {len(ciphertext)} bytes written back to {filename}")
    print(f"[+] Key used: {KEY}")
    print(f"[+] First 16 ciphertext bytes (hex): {ciphertext[:16].hex()}")

if __name__ == "__main__":
    main()
