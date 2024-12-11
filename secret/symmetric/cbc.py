from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64


class Cbc:
    def pad_pkcs7(self, src, block_size):
        return pad(src, block_size)

    def unpad_pkcs7(self, src, block_size):
        return unpad(src, block_size)

    def encrypt(self, plaintext: str, key: str, iv: str = ""):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_text = self.pad_pkcs7(plaintext, AES.block_size)
        cipher_text = cipher.encrypt(padded_text)
        return cipher_text

    def decrypt(self, ciphertext: str, key: str, iv: str = ""):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext)
        unpadded_text = self.unpad_pkcs7(plaintext, AES.block_size)
        return unpadded_text

    def demo():
        key = base64.b64decode("tjp5OPIU1ETF5s33fsLWdA==")
        iv = b"0987654321098765"

        cbc = Cbc()

        encrypted = cbc.encrypt(b"abcdefghijklmnopqrstuvwxyz", key, iv)
        base64_encoded = base64.b64encode(encrypted).decode("utf-8")
        print(f"[CBC] base64 encoded: {base64_encoded}")

        base64_decoded = base64.b64decode(base64_encoded)
        decrypted = cbc.decrypt(base64_decoded, key, iv)
        print(f"[CBC] decrypted: {decrypted.decode('utf-8')}")
