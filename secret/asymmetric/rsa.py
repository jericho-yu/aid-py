from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

class Rsa:
    """
    RSA Encryption and Decryption class
    """
    def __init__(self):
        pass

    def encrypt_by_base64(self, base64_public_key: str, plaintext: bytes) -> bytes:
        """
        Encrypt data using a Base64-encoded public key.
        """
        try:
            # Decode the Base64 public key
            pem_public_key = base64.b64decode(base64_public_key)
            return self.encrypt_by_pem(pem_public_key, plaintext)
        except Exception as e:
            raise ValueError(f"Error in encrypt_by_base64: {e}")

    def encrypt_by_pem(self, pem_public_key: bytes, plaintext: bytes) -> bytes:
        """
        Encrypt data using a PEM-encoded public key.
        """
        try:
            # Load the PEM public key
            public_key = serialization.load_pem_public_key(pem_public_key)
            # Encrypt the plaintext
            ciphertext = public_key.encrypt(
                plaintext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return ciphertext
        except Exception as e:
            raise ValueError(f"Error in encrypt_by_pem: {e}")

    def decrypt_by_base64(self, base64_private_key: str, ciphertext: bytes) -> bytes:
        """
        Decrypt data using a Base64-encoded private key.
        """
        try:
            # Decode the Base64 private key
            pem_private_key = base64.b64decode(base64_private_key)
            return self.decrypt_by_pem(pem_private_key, ciphertext)
        except Exception as e:
            raise ValueError(f"Error in decrypt_by_base64: {e}")

    def decrypt_by_pem(self, pem_private_key: bytes, ciphertext: bytes) -> bytes:
        """
        Decrypt data using a PEM-encoded private key.
        """
        try:
            # Load the PEM private key
            private_key = serialization.load_pem_private_key(pem_private_key, password=None)
            # Decrypt the ciphertext
            plaintext = private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            return plaintext
        except Exception as e:
            raise ValueError(f"Error in decrypt_by_pem: {e}")

# Example usage
rsa_instance = Rsa()
rsa_instance
