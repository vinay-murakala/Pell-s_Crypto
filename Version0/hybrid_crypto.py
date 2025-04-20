import tkinter as tk
from tkinter import messagebox
import base64
import math
import random
import sympy
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import secrets

class HybridCrypto:
    """Manages hybrid encryption/decryption using RSA, Pell's equation, and AES."""
    
    def __init__(self):
        self.primes = [x for x in range(100) if sympy.isprime(x)]
        self.N1 = self.e1 = self.d1 = self.phi1 = None
        self.N2 = self.e2 = self.d2 = self.phi2 = None
        self.E1 = self.E2 = None
        self.aes_key = None
        self.encrypted_aes_key = None

    def gcd(self, a, b):
        """Calculate the greatest common divisor of a and b."""
        while b:
            a, b = b, a % b
        return a

    def multiplicative_inverse(self, e, phi):
        """Find the modular inverse of e modulo phi using Extended Euclidean Algorithm."""
        d, x1, x2, y1 = 0, 0, 1, 1
        temp_phi = phi
        while e > 0:
            temp1 = temp_phi // e
            temp2 = temp_phi - temp1 * e
            temp_phi, e = e, temp2
            x = x2 - temp1 * x1
            y = d - temp1 * y1
            x2, x1, d, y1 = x1, x, y1, y
        return d + phi if temp_phi == 1 else None

    def generate_keypair(self):
        """Generate RSA key pair with 2048-bit modulus."""
        key_size = 2048
        p = sympy.randprime(2**(key_size//2), 2**(key_size//2+1))
        q = sympy.randprime(2**(key_size//2), 2**(key_size//2+1))
        n = p * q
        phi = (p - 1) * (q - 1)
        e = random.randrange(1, phi)
        while self.gcd(e, phi) != 1:
            e = random.randrange(1, phi)
        d = self.multiplicative_inverse(e, phi)
        return n, e, d, phi

    def solve_pell(self, n):
        """Solve Pell's equation x^2 - n*y^2 = 1 for the fundamental solution."""
        x = int(math.sqrt(n))
        y, z, r = x, 1, x << 1
        e1, e2 = 1, 0
        f1, f2 = 0, 1
        while True:
            y = r * z - y
            z = (n - y * y) // z
            r = (x + y) // z
            e1, e2 = e2, e1 + e2 * r
            f1, f2 = f2, f1 + f2 * r
            a, b = f2 * x + e2, f2
            if a * a - n * b * b == 1:
                return a, b

    def encrypt_text(self, plaintext):
        """Encrypt the plaintext using hybrid RSA and AES."""
        if not plaintext:
            raise ValueError("Input text cannot be empty")

        # Convert text to list of ASCII values
        ascii_values = [ord(c) for c in plaintext]

        # Generate two RSA key pairs
        self.N1, self.e1, self.d1, self.phi1 = self.generate_keypair()
        self.N2, self.e2, self.d2, self.phi2 = self.generate_keypair()

        # Select random primes for Pell's equation
        D1 = random.choice(self.primes)
        D2 = random.choice(self.primes)

        # Solve Pell's equation
        X1, Y1 = self.solve_pell(D1)
        X2, Y2 = self.solve_pell(D2)

        # Compute alpha values
        alpha1 = pow((self.phi1 + X1), 2) - (D1 * pow((self.e1 + Y1), 2))
        alpha2 = pow((self.phi2 + X2), 2) - (D2 * pow((self.e2 + Y2), 2))

        # Generate public keys
        K1 = ((alpha1 + (D1 * pow(self.e1, 2)) + (2 * D1 * self.e1 * Y1)) * pow(self.d1, 2)) % self.phi1
        K2 = ((alpha2 + (D2 * pow(self.e2, 2)) + (2 * D2 * self.e2 * Y2)) * pow(self.d2, 2)) % self.phi2

        # Generate private keys
        self.E1 = pow(self.e1, 2) % self.phi1
        self.E2 = pow(self.e2, 2) % self.phi2

        # Encrypt with both RSA key pairs
        C1 = self.rsa_encrypt_list(ascii_values, K1, self.N1)
        C2 = self.rsa_encrypt_list(ascii_values, K2, self.N2)
        asymmetric_cipher = f"{' '.join(map(str, C1))}^{' '.join(map(str, C2))}"

        # Generate and encrypt AES key
        self.aes_key = secrets.token_bytes(16)
        cipher = AES.new(self.aes_key, AES.MODE_CBC)
        iv = cipher.iv
        ciphertext = cipher.encrypt(pad(asymmetric_cipher.encode(), AES.block_size))
        symmetric_cipher = iv + ciphertext

        # Encrypt AES key with RSA (using first public key for simplicity)
        self.encrypted_aes_key = pow(int.from_bytes(self.aes_key, 'big'), self.e1, self.N1)

        return base64.b64encode(symmetric_cipher).decode()

    def decrypt_text(self, ciphertext, encrypted_aes_key):
        """Decrypt the ciphertext using hybrid RSA and AES."""
        if not ciphertext:
            raise ValueError("Ciphertext cannot be empty")

        try:
            # Decode and decrypt AES ciphertext
            symmetric_cipher = base64.b64decode(ciphertext)
            iv, ciphertext = symmetric_cipher[:16], symmetric_cipher[16:]

            # Decrypt AES key with RSA
            aes_key_int = pow(int(encrypted_aes_key), self.d1, self.N1)
            aes_key = aes_key_int.to_bytes(16, 'big')

            cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
            asymmetric_cipher = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

            # Split and decrypt the two RSA ciphertexts
            C1_str, C2_str = asymmetric_cipher.split('^')
            C1 = [int(i) for i in C1_str.split()]
            C2 = [int(i) for i in C2_str.split()]

            message1 = ''.join(chr(pow(c, self.E1, self.N1)) for c in C1)
            message2 = ''.join(chr(pow(c, self.E2, self.N2)) for c in C2)

            return message1 if message1 == message2 else "Cipher Corrupted"
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")

    def rsa_encrypt_list(self, values, key, modulus):
        """Encrypt a list of values using RSA."""
        return [pow(v, key, modulus) for v in values]

def create_gui():
    """Create and run the Tkinter GUI for encryption/decryption."""
    crypto = HybridCrypto()
    window = tk.Tk()
    window.geometry("375x550")
    window.title("Hybrid Crypto App")

    # Set icon (replace 'Keys.png' with actual path or remove if not needed)
    try:
        window.iconphoto(False, tk.PhotoImage(file="Keys.png"))
    except Exception:
        pass

    def encrypt_action():
        plaintext = input_text.get("1.0", tk.END).rstrip()
        try:
            ciphertext = crypto.encrypt_text(plaintext)
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, ciphertext)
            key_field.delete("1.0", tk.END)
            key_field.insert(tk.END, str(crypto.encrypted_aes_key))
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", "Encryption failed: Invalid input")

    def decrypt_action():
        ciphertext = input_text.get("1.0", tk.END).rstrip()
        encrypted_key = key_field.get("1.0", tk.END).rstrip()
        try:
            decrypted = crypto.decrypt_text(ciphertext, int(encrypted_key))
            output_text.delete("1.0", tk.END)
            output_text.insert(tk.END, decrypted)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", "Decryption failed: Invalid input or key")

    def reset_action():
        input_text.delete("1.0", tk.END)
        output_text.delete("1.0", tk.END)
        key_field.delete("1.0", tk.END)

    # GUI Elements
    tk.Label(window, text="Enter text for encryption/decryption", fg="black", font=("Calibri", 13)).place(x=10, y=10)
    input_text = tk.Text(window, font="Roboto 10", bg="white", relief=tk.GROOVE, wrap=tk.WORD, bd=0)
    input_text.place(x=10, y=50, width=355, height=100)

    tk.Label(window, text="RSA-encrypted AES key", fg="black", font=("Calibri", 13)).place(x=10, y=160)
    key_field = tk.Text(window, font="Roboto 10", bg="white", relief=tk.GROOVE, wrap=tk.WORD, bd=0)
    key_field.place(x=10, y=190, width=355, height=50)

    tk.Button(window, text="ENCRYPT", height=2, width=23, bg="#ed3833", fg="white", bd=0, command=encrypt_action).place(x=10, y=250)
    tk.Button(window, text="DECRYPT", height=2, width=23, bg="#00bd56", fg="white", bd=0, command=decrypt_action).place(x=200, y=250)
    tk.Button(window, text="RESET", height=2, width=50, bg="#1089ff", fg="white", bd=0, command=reset_action).place(x=10, y=300)

    tk.Label(window, text="Output", fg="black", font=("Calibri", 13)).place(x=10, y=350)
    output_text = tk.Text(window, font="Roboto 10", bg="white", relief=tk.GROOVE, wrap=tk.WORD, bd=0)
    output_text.place(x=10, y=380, width=355, height=150)

    window.mainloop()

if __name__ == "__main__":
    create_gui()