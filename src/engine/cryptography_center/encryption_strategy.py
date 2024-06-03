
from abc import ABC, abstractmethod

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes


class EncryptionStrategy(ABC):
    @abstractmethod
    def encrypt(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decrypt(self, data: bytes) -> bytes:
        pass


class AESEncryptionStrategy(EncryptionStrategy):
    def __init__(self, key: bytes):
        self.key = key
        self.iv = get_random_bytes(16)

    def encrypt(self, data: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_CFB, iv=self.iv)
        return self.iv + cipher.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        iv = data[:16]
        cipher = AES.new(self.key, AES.MODE_CFB, iv=iv)
        return cipher.decrypt(data[16:])


class RSAEncryptionStrategy(EncryptionStrategy):
    def __init__(self, public_key: RSA.RsaKey, private_key: RSA.RsaKey = None):
        self.public_key = public_key
        self.private_key = private_key

    def encrypt(self, data: bytes) -> bytes:
        cipher = PKCS1_OAEP.new(self.public_key)
        return cipher.encrypt(data)

    def decrypt(self, data: bytes) -> bytes:
        if self.private_key is None:
            raise ValueError('Private key is required for decryption')
        cipher = PKCS1_OAEP.new(self.private_key)
        return cipher.decrypt(data)
