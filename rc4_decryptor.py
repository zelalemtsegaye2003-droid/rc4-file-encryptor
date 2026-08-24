#!/usr/bin/env python3
"""
RC4 File Decryptor
Reads file.txt in binary mode, decrypts it with RC4, and restores the original contents.
"""

import sys

def rc4_ksa(key: bytes) -> list:
    """Key Scheduling Algorithm — identical to the encryptor."""
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) & 0xFF
        S[i], S[j] = S[j], S[i]
    return S

def rc4_prga(S: list, data_len: int) -> bytes:
    """Pseudo-Random Generation Algorithm — identical to the encryptor."""
    S = S[:]
    i = j = 0
    keystream = bytearray()
    for _ in range(data_len):
        i = (i + 1) & 0xFF
        j = (j + S[i]) & 0xFF
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) & 0xFF]
        keystream.append(K)
    return bytes(keystream)

def rc4_decrypt(key: bytes, ciphertext: bytes) -> bytes:
    """Decrypt data using RC4 (identical operation to encrypt — XOR with keystream)."""
    S = rc4_ksa(key)
    keystream = rc4_prga(S, len(ciphertext))
    return bytes(c ^ k for c, k in zip(ciphertext, keystream))

def main():
    KEY = b"p4ssw0rd"  # MUST match the encryptor's key
    
    filename = "file.txt"
    try:
        with open(filename, "rb") as f:
            ciphertext = f.read()
    except FileNotFoundError:
        print(f"[-] Error: {filename} not found in the current directory.")
        sys.exit(1)
    
    print(f"[+] Read {len(ciphertext)} bytes from {filename}")
    
    plaintext = rc4_decrypt(KEY, ciphertext)
    
    with open(filename, "wb") as f:
        f.write(plaintext)
    
    print(f"[+] Decrypted {len(plaintext)} bytes written back to {filename}")
    print(f"[+] Key used: {KEY}")
    print(f"[+] First 16 plaintext bytes (hex): {plaintext[:16].hex()}")
    print(f"[+] If the original file was text, preview: {plaintext[:64]}")

if __name__ == "__main__":
    main()
