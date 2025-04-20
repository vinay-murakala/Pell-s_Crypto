from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from src.key_generation import generate_keys
from src.utils import modular_exp
import secrets
import struct

def encrypt_message(message, output_file):
    # Convert message to bytes
    message_bytes = message.encode('utf-8')

    # Generate keys
    public_key, private_key, n, phi = generate_keys()
    e, n = public_key

    # Generate symmetric key
    aes_key = secrets.token_bytes(32)  # 256-bit AES key

    # Encrypt AES key with public key (RSA)
    aes_key_int = int.from_bytes(aes_key, 'big')
    if aes_key_int >= n:
        raise ValueError("AES key too large for modulus")
    cipher_key = modular_exp(aes_key_int, e, n)

    # Encrypt message with AES
    iv = get_random_bytes(16)
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    ciphertext = cipher_aes.encrypt(pad(message_bytes, AES.block_size))

    # Write to file: [key_length, cipher_key, iv, ciphertext]
    cipher_key_bytes = cipher_key.to_bytes((cipher_key.bit_length() + 7) // 8, 'big')
    cipher_key_length = len(cipher_key_bytes)
    
    with open(output_file, 'wb') as f:
        f.write(struct.pack('<I', cipher_key_length))
        f.write(cipher_key_bytes)
        f.write(iv)
        f.write(ciphertext)

    # Save private key (securely in practice)
    with open('private_key.bin', 'wb') as f:
        d_bytes = private_key[0].to_bytes((private_key[0].bit_length() + 7) // 8, 'big')
        n_bytes = private_key[1].to_bytes((private_key[1].bit_length() + 7) // 8, 'big')
        f.write(len(d_bytes).to_bytes(4, 'big'))
        f.write(d_bytes)
        f.write(n_bytes)