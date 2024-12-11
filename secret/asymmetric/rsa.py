from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from secret.asymmetric.pem import PemBase64


class Rsa:
    def __init__(self, pem: PemBase64):
        self.pem = pem

    def set_pem(self, pem: PemBase64) -> "Rsa":
        """
        设置 PEM 编码的密钥。

        参数:
        pem (PemBase64): PEM 编码的密钥对象。

        返回:
        Rsa: 当前 Rsa 对象。
        """
        self.pem = pem
        return self

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        使用 PEM 编码的公钥加密明文。

        参数:
        plaintext (bytes): 需要加密的明文数据。

        返回:
        bytes: 加密后的密文。
        """
        ciphertext = serialization.load_pem_public_key(
            self.pem.generate_pem_public_key().get_pem_public_key()
        ).encrypt(
            plaintext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return ciphertext

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        使用 PEM 私钥解密密文。

        参数:
        ciphertext (bytes): 需要解密的密文。

        返回:
        bytes: 解密后的明文。

        异常:
        ValueError: 当解密过程中发生错误时抛出异常。
        """
        try:
            private_key = serialization.load_pem_private_key(
                self.pem.generate_pem_private_key().get_pem_private_key(),
                password=None,
            )
            plaintext = private_key.decrypt(
                ciphertext,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None,
                ),
            )
            return plaintext
        except Exception as e:
            raise ValueError(f"Error in decrypt_by_pem: {e}")

    @staticmethod
    def demo():
        pem = PemBase64()
        pem.set_base64_public_key(
            "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCFbbjNGuqhF3HhmvnZxjG6mS6Q3OmD/vh9voriZTyNCVLJ7y2r0bHZZ7brWwkgtGPQXosZ0IzUZAvlMuZ0m11DiuXZzlCnRz1owwMXKalJeeKQwA8CoJBSy99zCo9fxIErqTMhGwPFCKUaByt8TEIkNq8fUsmqjqqshRLKSazWuwIDAQAB"
        ).set_base64_private_key(
            "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGBAIVtuM0a6qEXceGa+dnGMbqZLpDc6YP++H2+iuJlPI0JUsnvLavRsdlntutbCSC0Y9BeixnQjNRkC+Uy5nSbXUOK5dnOUKdHPWjDAxcpqUl54pDADwKgkFLL33MKj1/EgSupMyEbA8UIpRoHK3xMQiQ2rx9SyaqOqqyFEspJrNa7AgMBAAECgYATaA4E5vFRVNOfeKb2YblB5p27PCZKqH8D6v7QRuEzsjN0Y3FFGE7BzC/ys170fsg1ukqJCqgxDAwe3fRe6Wn6/Y5IEF/wRYODQn6yAXhCUepheaRl9zK+P+XXbGWENdL2N/KchNZrKUF97Eu00OhBI7uEKpUrhPuzaYDPiHujQQJBAOvc+Xwz3j/srv26bk5UJOAJtU096pNseEeVzFqSTU903NdgFUQupTsPeokUtMBeMihAYlfDZypIK0kvBoymTNkCQQCQ0e/vEGnqh9C0y340HUlIZe0Q5mAJ5e+3a7lR21LS9ki5vQLUf2Wjxw/QVbPDZthGK33BusrobyuwcVOMmROzAkEAz9lefeZTb6/Kkcvtktcx28CSZawvgJTw9dx7RkFxIZkRWDbS5s/YSdCdIhn+IxufRbtfLooC6s7IXmizc9TFGQJAZP1hum7RzbFkg4+ctK7vmcMqbKyasIxefKRsmX6+5UrGMHB0dsdYk7uPdZMuRseDbnuJuP2P3kMYTnTY9KUTLQJANq7Cy5OjtHiJ5EsRBePfGm9Qvs3mwJZAKDpZsmTRSyaQCTCpL6RQ+7gVFIEmiEU4REjag9/aq8C1G0MyvwxkiA=="
        )
        rsa = Rsa(pem=pem)
        ciphertext = rsa.encrypt(plaintext=b"hello world")
        print(ciphertext)

        plaintext = rsa.decrypt(ciphertext=ciphertext)
        print(plaintext)
