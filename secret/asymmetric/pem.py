import base64
from Crypto.PublicKey import RSA

class PemBase64:
    def __init__(self):
        self.base64_public_key = ""
        self.base64_private_key = ""
        self.public_key = None
        self.private_key = None

    def set_base64_public_key(self, base64_public_key):
        self.base64_public_key = base64_public_key
        return self

    def set_base64_private_key(self, base64_private_key):
        self.base64_private_key = base64_private_key
        return self

    def get_pem_public_key(self):
        return self.public_key

    def get_pem_private_key(self):
        return self.private_key

    def generate_pem_public_key(self):
        public_key_bytes = base64.b64decode(self.base64_public_key)
        self.public_key = RSA.import_key(public_key_bytes)
        return self

    def generate_pem_private_key(self):
        private_key_bytes = base64.b64decode(self.base64_private_key)
        self.private_key = RSA.import_key(private_key_bytes)
        return self