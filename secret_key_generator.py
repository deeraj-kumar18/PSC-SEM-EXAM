import os

# Generate a random key with 24 bytes of entropy
secret_key = os.urandom(24)

# Convert the bytes to a string in hexadecimal format
secret_key_hex = secret_key.hex()

print("Generated secret key:", secret_key_hex)

# Generated secret key: 9fce27c5bd0b2ba35607b8dafafed0021875a46ef656c7ea