import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from secret.symmetric.aes import Aes


class Ecb:
    def __init__(self, aes: Aes):
        self.aes_encrypt = aes.new_encrypt().get_encrypt()
        self.open_key = self.aes_encrypt.get_open_key()
        self.aes_decrypt = aes.new_decrypt(open_key=self.open_key).get_decrypt()

    def encrypt(self, plaintext: str) -> bytes:
        cipher = AES.new(self.open_key.encode(), AES.MODE_ECB)
        return  cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    
    def decrypt(self,encrypted:bytes)->str:
        cipher = AES.new(self.open_key.encode(),AES.MODE_ECB)
        return unpad(cipher.decrypt(encrypted),AES.block_size)
    
    @staticmethod
    def demo():
        ecb = Ecb(Aes(sail="tjp5OPIU1ETF5s33fsLWdA=="))
        data = [{"name":"张三","age":18},{"name":"李四","age":20}]
        encrypted = ecb.encrypt(json.dumps(data))
        print(f"encrypted: {encrypted}")
        
        decrypted = ecb.decrypt(encrypted)
        print(f"decrypted: {decrypted}")
        

# # 示例用法
# key = b"Sixteen byte key"  # 密钥必须是16, 24或32字节长
# data = b"This is some data to encrypt"

# encrypted_data = ecb_encrypt(key, data)
# print(f"Encrypted: {encrypted_data}")

# decrypted_data = ecb_decrypt(key, encrypted_data)
# print(f"Decrypted: {decrypted_data}")
