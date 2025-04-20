import pytest
from src.encryption import encrypt_message
from src.decryption import decrypt_message
import os

def test_encrypt_decrypt():
    message = "Hello, World!"
    ciphertext_file = "test_ciphertext.bin"
    output_file = "test_plaintext.txt"

    # Encrypt
    encrypt_message(message, ciphertext_file)
    assert os.path.exists(ciphertext_file)
    assert os.path.exists("private_key.bin")

    # Decrypt
    plaintext = decrypt_message(ciphertext_file)
    assert plaintext == message

    # Clean up
    os.remove(ciphertext_file)
    os.remove("private_key.bin")
