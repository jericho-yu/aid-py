from secret.asymmetric.rsa import Rsa
from secret.asymmetric.pem import PemBase64

if __name__ == "__main__":
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
    
