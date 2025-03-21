from cryptography.fernet import Fernet

def newKey() -> bytes:
    key = Fernet.generate_key()
    return key

def createChipher(key: bytes) -> object:
    cipher = Fernet(key)
    return cipher

def encrypt(cipher: object, plainText: bytes) -> bytes:
    cryptoText = cipher.encrypt(plainText)
    return cryptoText

def decrypt(cipher: object, cryptoText: str | bytes, byteMode=False) -> str | bytes:
    if byteMode == True:
        plainText = cipher.decrypt(cryptoText)
    else:
        plainText = cipher.decrypt(cryptoText).decode()
    return plainText

def encryptString(plainText: str, key=b'N4c4aAnEyqjpvIzXD9wZ7doo5V6WOUGi7xvyxBq3gSA=') -> str:
    cihperEngine = createChipher(key)
    byteForm = plainText.encode()
    cryptoText = encrypt(cihperEngine, byteForm).decode()
    return cryptoText

def decryptString(cryptoText: str | bytes, key=b'N4c4aAnEyqjpvIzXD9wZ7doo5V6WOUGi7xvyxBq3gSA=') -> str:
    cipherEnginge = createChipher(key)
    plainText = decrypt(cipherEnginge, cryptoText)
    return plainText

if __name__ == "__main__":

    secretKey = newKey()
    # print(secretKey)

    secretChipher = createChipher(secretKey)
    # print(secretChipher)

    newEncrypt = encrypt(secretChipher, b'Karhu')
    # print(newEncrypt)

    newDecrypt = decrypt(secretChipher, newEncrypt)
    # print(newDecrypt)

    encryptReady = encryptString('Papukaija')
    # print(encryptReady)

    decryptReady = decryptString(encryptReady)
    # print(decryptReady)