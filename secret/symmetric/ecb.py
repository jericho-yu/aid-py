from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from secret.symmetric.aes import Aes


class Ecb:
    def __init__(self, aes: Aes):
        self.aes_encrypt = aes.new_encrypt().get_encrypt()
        self.open_key = self.aes_encrypt.get_open_key()
        self.aes_key_str = self.aes_encrypt.get_aes_key_str()
        self.aes_decrypt = aes.new_decrypt(open_key=self.open_key).get_decrypt()
        aes_key_str = self.aes_decrypt.de_sail_by_byte().get_aes_key_str()
        if self.aes_key_str != aes_key_str:
            raise Exception("aes key 验证错误")
        open_key2 = aes_decrypt.get_open_key()

def ecb_encrypt(key, data):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return encrypted_data


def ecb_decrypt(key, encrypted_data):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data


# 示例用法
key = b"Sixteen byte key"  # 密钥必须是16, 24或32字节长
data = b"This is some data to encrypt"

encrypted_data = ecb_encrypt(key, data)
print(f"Encrypted: {encrypted_data}")

decrypted_data = ecb_decrypt(key, encrypted_data)
print(f"Decrypted: {decrypted_data}")
