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


if __name__ == "__main__":
    pem = PemBase64()
    pem.set_base64_public_key(
        "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCFbbjNGuqhF3HhmvnZxjG6mS6Q3OmD/vh9voriZTyNCVLJ7y2r0bHZZ7brWwkgtGPQXosZ0IzUZAvlMuZ0m11DiuXZzlCnRz1owwMXKalJeeKQwA8CoJBSy99zCo9fxIErqTMhGwPFCKUaByt8TEIkNq8fUsmqjqqshRLKSazWuwIDAQAB"
    )
    rsa = Rsa(pem)
    ciphertext = rsa.encrypt(plaintext=b"hello world")
