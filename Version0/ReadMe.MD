# Hybrid Crypto App

A Python application that performs hybrid encryption and decryption using RSA, Pell's equation, and AES, with a user-friendly Tkinter GUI. The app encrypts text using two RSA key pairs, derives additional keys via Pell's equation, and applies AES encryption for the final ciphertext. Decryption reverses the process, ensuring data integrity by comparing results from both RSA key pairs.

## Features

- **Hybrid Encryption**: Combines RSA (asymmetric) and AES (symmetric) encryption for secure data processing.
- **Pell's Equation**: Uses solutions to Pell's equation for RSA key derivation (experimental).
- **GUI Interface**: Tkinter-based interface for easy encryption, decryption, and key management.
- **Secure Key Handling**: Generates 2048-bit RSA keys and encrypts AES keys with RSA for secure sharing.
- **Error Handling**: Validates inputs and provides user-friendly error messages.

## Prerequisites

- **Python 3.8+**
- **Required Libraries**:
  - `pycryptodome` (for AES encryption)
  - `sympy` (for prime number generation and Pell's equation)
  - `tkinter` (included with standard Python for GUI)

Install dependencies using pip:

```bash
pip install pycryptodome sympy
```

## Setup

1. **Clone or Download**:

   - Download the project files, including `hybrid_crypto.py` and (optionally) `Keys.png` for the GUI icon.
   - Place `Keys.png` in the same directory as `hybrid_crypto.py` or update the icon path in the code.

2. **Verify Dependencies**:

   - Ensure Python and the required libraries are installed.
   - Run `pip show pycryptodome sympy` to confirm.

3. **Run the Application**:

   - Execute the script:

     ```bash
     python hybrid_crypto.py
     ```

## Usage

1. **Launch the App**:

   - Run the script to open the Tkinter GUI.

2. **Encrypt Text**:

   - Enter text in the "Enter text for encryption/decryption" field.
   - Click **ENCRYPT** to generate:
     - A base64-encoded ciphertext (displayed in the "Output" field).
     - An RSA-encrypted AES key (displayed in the "RSA-encrypted AES key" field).
   - Copy both outputs for decryption.

3. **Decrypt Text**:

   - Paste the base64-encoded ciphertext into the input field.
   - Paste the RSA-encrypted AES key into the key field.
   - Click **DECRYPT** to retrieve the original text or see "Cipher Corrupted" if decryption fails.

4. **Reset**:

   - Click **RESET** to clear all fields.

## Example

- **Input Text**: `Hello, World!`
- **Encrypt Output**:
  - Ciphertext: `Y2lwaGVydGV4dC1iYXNlNjQtc3RyaW5n...`
  - Encrypted AES Key: `123456789...` (large integer)
- **Decrypt**:
  - Paste the ciphertext and key, then click **DECRYPT**.
  - Output: `Hello, World!` (or "Cipher Corrupted" if invalid).

## Notes

- **Security**:
  - Uses 2048-bit RSA keys for strong asymmetric encryption.
  - AES operates in CBC mode with a random IV for each encryption.
  - The AES key is encrypted with RSA for secure sharing.
- **Limitations**:
  - Decryption currently works within the same session due to in-memory key storage. For cross-session decryption, persist RSA private keys securely (e.g., to a file).
  - Pell's equation-based key derivation is experimental and may not enhance security; consider standard RSA+AES for production use.
- **Performance**:
  - Large RSA keys (2048 bits) ensure security but may slow encryption/decryption compared to smaller keys.

## Project Structure

- `hybrid_crypto.py`: Main application script containing the encryption logic and GUI.
- `Keys.png` (optional): Icon file for the GUI (replace with your own or remove the icon code).

## Future Improvements

- **Key Persistence**: Save RSA private keys to a file or database for cross-session decryption.
- **Simplified Crypto**: Replace Pell's equation with standard RSA key exchange for better performance and clarity.
- **Enhanced GUI**: Add options to save/load keys or display encryption parameters.
- **Input Validation**: Further restrict input characters or add length limits.

## License

This project is for educational purposes and provided as-is. Use at your own risk.

## Contact

For questions or contributions, please open an issue or contact the maintainer.