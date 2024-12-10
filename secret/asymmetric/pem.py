import base64
import pem
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend


class PemBase64:
    def __init__(self):
        self.base64_public_key = ""
        self.base64_private_key = ""
        self.public_key = None
        self.private_key = None

    def set_base64_public_key(self, base64_public_key) -> "PemBase64":
        self.base64_public_key = base64_public_key
        return self

    def set_base64_private_key(self, base64_private_key) -> "PemBase64":
        self.base64_private_key = base64_private_key
        return self

    def get_base64_public_key(self) -> str:
        return self.base64_public_key

    def get_base64_private_key(self) -> str:
        return self.base64_private_key

    def get_pem_public_key(self) -> bytes:
        return self.public_key

    def get_pem_private_key(self) -> bytes:
        return self.private_key

    def generate_pem_public_key(self) -> "PemBase64":
        try:
            public_key_bytes = base64.b64decode(self.base64_public_key)
        except Exception as e:
            raise ValueError(f"解码Base64失败: {e}")

        try:
            public_key = serialization.load_der_public_key(
                public_key_bytes, backend=default_backend()
            )
            pem_public_key = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            self.public_key = pem_public_key
        except Exception as e:
            raise ValueError(f"解析公钥失败: {e}")

        return self

    def generate_pem_private_key(self) -> "PemBase64":
        try:
            private_key_bytes = base64.b64decode(self.base64_private_key)
        except Exception as e:
            raise ValueError(f"解码Base64失败: {e}")

        try:
            private_key = serialization.load_der_private_key(
                private_key_bytes, password=None, backend=default_backend()
            )
            pem_private_key = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
            self.private_key = pem_private_key
        except Exception as e:
            raise ValueError(f"解析私钥失败: {e}")

        return self
