from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from src.utils import modular_exp
import struct

def decrypt_message(ciphertext_file):
    # Read private key
    with open('private_key.bin', 'rb') as f:
        d_length = int.from_bytes(f.read(4), 'big')
        d = int.from_bytes(f.read(d_length), 'big')
        n = int.from_bytes(f.read(), 'big')
    private_key = (d, n)

    # Read ciphertext file
    with open(ciphertext_file, 'rb') as f:
        key_length = struct.unpack('<I', f.read(4))[0]
        cipher_key_bytes = f.read(key_length)
        iv = f.read(16)
        ciphertext = f.read()

    # Decrypt AES key
    cipher_key = int.from_bytes(cipher_key_bytes, 'big')
    aes_key_int = modular_exp(cipher_key, private_key[0], private_key[1])
    aes_key = aes_key_int.to_bytes(32, 'big')

    # Decrypt message with AES
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    padded_plaintext = cipher_aes.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext, AES.block_size)

    return plaintext.decode('utf-8')