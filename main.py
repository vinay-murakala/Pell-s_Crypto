import argparse
from src.encryption import encrypt_message
from src.decryption import decrypt_message

def main():
    parser = argparse.ArgumentParser(description="Pell's Equation Encryption/Decryption App")
    parser.add_argument('--mode', choices=['encrypt', 'decrypt'], required=True, help="Mode: encrypt or decrypt")
    parser.add_argument('--message', type=str, help="Message to encrypt (for encrypt mode)")
    parser.add_argument('--ciphertext', type=str, help="Ciphertext file to decrypt (for decrypt mode)")
    parser.add_argument('--output', type=str, default="output.bin", help="Output file for ciphertext or plaintext")
    
    args = parser.parse_args()

    if args.mode == 'encrypt':
        if not args.message:
            print("Error: --message is required for encryption")
            return
        encrypt_message(args.message, args.output)
        print(f"Encryption complete. Ciphertext saved to {args.output}")
    elif args.mode == 'decrypt':
        if not args.ciphertext:
            print("Error: --ciphertext is required for decryption")
            return
        plaintext = decrypt_message(args.ciphertext)
        with open(args.output, 'w') as f:
            f.write(plaintext)
        print(f"Decryption complete. Plaintext saved to {args.output}")

if __name__ == '__main__':
    main()
