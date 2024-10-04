import hashlib
from cryptography.fernet import Fernet

# Class to manage data protection
class DataProtection:
    def __init__(self, key):
        # Initialize the encryption tool with the provided key
        self.cipher_suite = Fernet(key)

    @staticmethod
    def generate_key():
        # Generate a new encryption key
        return Fernet.generate_key()

    def encrypt_data(self, data):
        # Encrypt the data if it is not empty
        if data:
            return self.cipher_suite.encrypt(data.encode())
        return None

    def decrypt_data(self, encrypted_data):
        # Decrypt the data if it is not empty
        if encrypted_data:
            return self.cipher_suite.decrypt(encrypted_data).decode()
        return None

    @staticmethod
    def pseudonymize_data(data):
        # Pseudonymize the data using a SHA-256 hash
        if data:
            return hashlib.sha256(data.encode()).hexdigest()
        return None
