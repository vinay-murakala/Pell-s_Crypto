# Pell's Crypto App

A Python application that implements a hybrid encryption system using standard RSA for key generation and AES for symmetric encryption.

## Features

- Generates RSA public/private keys for secure key exchange.
- Encrypts messages with AES using a symmetric key (protected by RSA encryption).
- Supports command-line interface for encryption and decryption.
- Includes unit tests and CI pipeline via GitHub Actions.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/vinay-murakala/Pell's_Crypto.git
   cd Pell's_Crypto
   ```

2. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Encrypt a Message

```bash
python main.py --mode encrypt --message "Hello, World!" --output ciphertext.bin
```

This encrypts the message and saves the ciphertext to `ciphertext.bin`. The private key is saved to `private_key.bin`.

### Decrypt a Message

```bash
python main.py --mode decrypt --ciphertext ciphertext.bin --output plaintext.txt
```

This decrypts the ciphertext and saves the plaintext to `plaintext.txt`.

### Run Tests

```bash
pytest tests
```

### Run Linting

```bash
flake8 src tests
```

## Project Structure

```
Pell's_Crypto/
├── .github/workflows/ci.yml       # GitHub Actions CI pipeline
├── src/                           # Source code
│   ├── __init__.py
│   ├── pells_equation.py          # Pell's equation solver (not currently used)
│   ├── key_generation.py          # RSA key generation logic
│   ├── encryption.py              # Encryption logic
│   ├── decryption.py              # Decryption logic
│   └── utils.py                   # Utility functions
├── tests/                         # Unit tests
│   ├── __init__.py
│   ├── test_pells_equation.py
│   └── test_encryption_decryption.py
├── main.py                        # CLI entry point
├── requirements.txt               # Dependencies
├── README.md                      # Project documentation
├── setup.py                       # Package setup
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore file
└── CHANGELOG.md                   # Version history
```

## Deployment to GitHub

1. **Create a Repository**:

   - Go to GitHub and create a new repository named `Pell's_Crypto`.
   - Initialize it without a README, .gitignore, or license (we’ll add these).

2. **Push the Code**:

   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/vinay-murakala/Pell's_Crypto.git
   git push -u origin main
   ```

3. **Verify CI Pipeline**:

   - Check the "Actions" tab on GitHub to ensure the CI workflow runs successfully.
   - The pipeline runs tests and linting on every push/pull request.

## Notes

- **Security**: This is an educational implementation using standard RSA and AES. For production, use established libraries like `cryptography` or `pycryptodome`.
- **Private Key**: The private key is saved to `private_key.bin` for simplicity. In production, use a secure key management system.
- **Pell's Equation**: The current implementation uses standard RSA instead of Pell's equation-based key generation for simplicity and reliability. The `pells_equation.py` module is included but not used.
- **Extending**: Modify the `bits` parameter in `key_generation.py` to experiment with different RSA key sizes (e.g., 2048-bit or 4096-bit).

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.
