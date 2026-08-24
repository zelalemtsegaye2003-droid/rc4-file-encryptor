# RC4 File Encryptor / Decryptor

A Python implementation of the **RC4 stream cipher** that encrypts and decrypts files.

## How It Works

- **RC4 KSA (Key Scheduling Algorithm)** — scrambles a 256-byte array using the key
- **RC4 PRGA (Pseudo-Random Generation Algorithm)** — generates a keystream
- **XOR** — plaintext XOR keystream = ciphertext (encryption)
- **XOR** — ciphertext XOR keystream = plaintext (decryption, same operation)

## Usage

```bash
# Encrypt file.txt
python3 rc4_encryptor.py

# Decrypt file.txt
python3 rc4_decryptor.py
