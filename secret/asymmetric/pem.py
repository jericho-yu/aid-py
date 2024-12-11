import base64
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


if __name__ == "__main__":
    pem = PemBase64()
    
    pem.set_base64_public_key(
        "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCFbbjNGuqhF3HhmvnZxjG6mS6Q3OmD/vh9voriZTyNCVLJ7y2r0bHZZ7brWwkgtGPQXosZ0IzUZAvlMuZ0m11DiuXZzlCnRz1owwMXKalJeeKQwA8CoJBSy99zCo9fxIErqTMhGwPFCKUaByt8TEIkNq8fUsmqjqqshRLKSazWuwIDAQAB"
    )
    print(pem.generate_pem_public_key().get_pem_public_key())
    
    pem.set_base64_private_key(
        "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAIVtuM0a6qEXceGa+dnGMbqZLpDc6YP++H2+iuJlPI0JUsnvLavRsdlntutbCSC0Y9BeixnQjNRkC+Uy5nSbXUOK5dnOUKdHPWjDAxcpqUl54pDADwKgkFLL33MKj1/EgSupMyEbA8UIpRoHK3xMQiQ2rx9SyaqOqqyFEspJrNa7AgMBAAECgYATaA4E5vFRVNOfeKb2YblB5p27PCZKqH8D6v7QRuEzsjN0Y3FFGE7BzC/ys170fsg1ukqJCqgxDAwe3fRe6Wn6/Y5IEF/wRYODQn6yAXhCUepheaRl9zK+P+XXbGWENdL2N/KchNZrKUF97Eu00OhBI7uEKpUrhPuzaYDPiHujQQJBAOvc+Xwz3j/srv26bk5UJOAJtU096pNseEeVzFqSTU903NdgFUQupTsPeokUtMBeMihAYlfDZypIK0kvBoymTNkCQQCQ0e/vEGnqh9C0y340HUlIZe0Q5mAJ5e+3a7lR21LS9ki5vQLUf2Wjxw/QVbPDZthGK33BusrobyuwcVOMmROzAkEAz9lefeZTb6/Kkcvtktcx28CSZawvgJTw9dx7RkFxIZkRWDbS5s/YSdCdIhn+IxufRbtfLooC6s7IXmizc9TFGQJAZP1hum7RzbFkg4+ctK7vmcMqbKyasIxefKRsmX6+5UrGMHB0dsdYk7uPdZMuRseDbnuJuP2P3kMYTnTY9KUTLQJANq7Cy5OjtHiJ5EsRBePfGm9Qvs3mwJZAKDpZsmTRSyaQCTCpL6RQ+7gVFIEmiEU4REjag9/aq8C1G0MyvwxkiA=="
    )
    print(pem.generate_pem_private_key().get_pem_private_key())
