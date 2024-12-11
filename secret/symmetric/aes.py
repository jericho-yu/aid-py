import base64
import os


class Aes:
    def __init__(self, sail):
        self.err = None
        self.encrypt = None
        self.decrypt = None
        self.sail_str = sail

    def new_encrypt(self) -> "Aes":
        self.encrypt = AesEncrypt(self.sail_str)
        return self

    def new_decrypt(self, open_key) -> "Aes":
        self.decrypt = AesDecrypt(self.sail_str, open_key)
        return self

    def get_encrypt(self) -> "AesEncrypt":
        return self.encrypt

    def get_decrypt(self) -> "AesDecrypt":
        return self.decrypt

    @staticmethod
    def demo():
        aes = Aes("tjp5OPIU1ETF5s33fsLWdA==")

        aes_encrypt = aes.new_encrypt().get_encrypt()
        open_key = aes_encrypt.get_open_key()
        aes_key_str = aes_encrypt.get_aes_key_str()
        print(f"aesKey: {aes_key_str}", f"openKey: {open_key}")

        aes_decrypt = aes.new_decrypt(open_key=open_key).get_decrypt()
        aes_key_str2 = aes_decrypt.de_sail_by_byte().get_aes_key_str()
        open_key2 = aes_decrypt.get_open_key()
        print(f"aesKey2: {aes_key_str2}", f"openKey2: {open_key2}")


class AesEncrypt:
    def __init__(self, sail):
        self.err = None
        self.sail_str = sail
        self.sail_byte = b""
        self.rand_key = b""
        self.aes_key = b""
        self.open_key = ""

        self.rand_key = os.urandom(16)
        try:
            self.sail_byte = base64.b64decode(sail)
        except Exception as e:
            self.err = e

        self.sail_by_byte()

    def sail_by_byte(self) -> "AesEncrypt":
        self.aes_key = bytearray(self.rand_key)

        for i in range(4):
            index = self.rand_key[i] % 16
            self.aes_key[index] = self.sail_byte[index]

        self.open_key = base64.b64encode(self.rand_key).decode("utf-8")
        return self

    def get_aes_key(self) -> bytes:
        return bytes(self.aes_key)

    def get_aes_key_str(self) -> str:
        return base64.b64encode(self.aes_key).decode("utf-8")

    def set_aes_key(self, aes_key) -> "AesEncrypt":
        self.aes_key = aes_key
        return self

    def get_open_key(self) -> str:
        return self.open_key


class AesDecrypt:
    def __init__(self, sail_str, open_key):
        self.err = None
        self.sail_str = sail_str
        self.sail_byte = b""
        self.rand_key = b""
        self.aes_key = b""
        self.open_key = open_key

        try:
            self.rand_key = base64.b64decode(open_key)
            self.sail_byte = base64.b64decode(sail_str)
        except Exception as e:
            self.err = e

        self.de_sail_by_byte()

    def de_sail_by_byte(self) -> "AesDecrypt":
        index = self.rand_key[:4]

        aes_key = bytearray(self.rand_key)
        for x in index:
            i = x % 16
            aes_key[i] = self.sail_byte[i]

        self.aes_key = bytes(aes_key)
        return self

    def get_aes_key(self) -> bytes:
        return self.aes_key

    def get_aes_key_str(self) -> str:
        return base64.b64encode(self.aes_key).decode("utf-8")

    def set_aes_key(self, aes_key) -> "AesDecrypt":
        self.aes_key = aes_key
        return self

    def get_open_key(self) -> str:
        return self.open_key
