import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from secret.symmetric.aes import Aes
from compression.zlib import Zlib


class Ecb:
    @staticmethod
    def encrypt(self, aes_key: bytes, plaintext: bytes) -> bytes:
        cipher = AES.new(aes_key, AES.MODE_ECB)
        return cipher.encrypt(pad(plaintext, AES.block_size))

    @staticmethod
    def decrypt(self, aes_key: bytes, encrypted: bytes) -> str:
        cipher = AES.new(aes_key, AES.MODE_ECB)
        return unpad(cipher.decrypt(encrypted), AES.block_size)

    @staticmethod
    def demo():
        aes = Aes(sail="tjp5OPIU1ETF5s33fsLWdA==")
        aes_encrypt = aes.new_encrypt().get_encrypt()
        open_key = aes_encrypt.get_open_key()
        aes_decrypt = aes.new_decrypt(open_key=open_key).get_decrypt()

        plaintext = json.dumps(
            [{"name": "张三", "age": 18}, {"name": "李四", "age": 20}]
        )

        # encrypt step1: zip
        zipped = Zlib.compress(plaintext)

        # encrypt step2: encrypt
        encrypted = Ecb.encrypt(aes_key=aes_encrypt.get_aes_key(), plaintext=zipped)
        
        base64Encoded = base64.b64encode(encrypted).decode("utf-8")
        print("encrypted: {base64Encoded}")
        
        # decrypt step1: decrypt
        decrypted = Ecb.decrypt(aes_key=aes_decrypt.get_aes_key(), encrypted=encrypted)
        
        # decrypt step2: decompress
        decompressed = Zlib.decompress(decrypted)
        print(f"decrypted: {decompressed}")


# # 示例用法
# key = b"Sixteen byte key"  # 密钥必须是16, 24或32字节长
# data = b"This is some data to encrypt"

# encrypted_data = ecb_encrypt(key, data)
# print(f"Encrypted: {encrypted_data}")

# decrypted_data = ecb_decrypt(key, encrypted_data)
# print(f"Decrypted: {decrypted_data}")
