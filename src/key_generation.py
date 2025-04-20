from Crypto.Util.number import getPrime

def generate_keys(bits=1024):
    # Generate large random primes
    p = getPrime(bits)
    q = getPrime(bits)
    
    # Calculate modulus and totient
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Standard RSA key generation
    e = 65537  # Common public exponent
    d = pow(e, -1, phi)  # Private exponent
    
    public_key = (e, n)
    private_key = (d, n)
    return public_key, private_key, n, phi