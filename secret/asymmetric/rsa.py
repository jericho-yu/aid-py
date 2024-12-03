import base64
import json
import zlib
from Crypto.Cipher import PKCS1_OAEP
import pem


class RsaHelper:
    @staticmethod
    def encrypt_by_pem(public_key, data):
        cipher = PKCS1_OAEP.new(public_key)
        return cipher.encrypt(data)

    @staticmethod
    def decrypt_by_pem(private_key, encrypted_data):
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(encrypted_data)


class Rsa:
    def demo_encrypt_rsa(self, un_encrypt):
        base64_public_key = "your_base64_public_key_here"
        pem_base64 = (
            pem.PemBase64()
            .set_base64_public_key(base64_public_key)
            .generate_pem_public_key()
        )
        pem_public_key = pem_base64.get_pem_public_key()

        encrypted = RsaHelper.encrypt_by_pem(pem_public_key, un_encrypt)
        base64_encrypted = base64.b64encode(encrypted).decode("utf-8")
        return base64_encrypted

    def demo_decrypt_rsa(self, base64_encrypted):
        base64_private_key = "your_base64_private_key_here"
        pem_base64 = (
            pem.PemBase64()
            .set_base64_private_key(base64_private_key)
            .generate_pem_private_key()
        )
        pem_private_key = pem_base64.get_pem_private_key()

        encrypted = base64.b64decode(base64_encrypted)
        decrypted = RsaHelper.decrypt_by_pem(pem_private_key, encrypted)
        return decrypted.decode("utf-8")

    def demo(self):
        un_encrypt = {
            "Username": "cbit",
            "Password": "cbit-pwd",
            "AesKey": "87dwQRkoNFNoIcq1A+zFHA==",
        }

        json_byte = json.dumps(un_encrypt).encode("utf-8")
        zip_byte = zlib.compress(json_byte)

        base64_encrypted = self.demo_encrypt_rsa(zip_byte)
        print(f"[RSA] encrypting: {base64_encrypted}")

        decrypted = self.demo_decrypt_rsa(base64_encrypted)
        print("[RSA] decrypted")

        unzip_byte = zlib.decompress(decrypted.encode("utf-8"))
        print(f"[RSA] decrypted: {unzip_byte.decode('utf-8')}")


if __name__ == "__main__":
    # Example usage
    rsa = Rsa()
    rsa.demo()
