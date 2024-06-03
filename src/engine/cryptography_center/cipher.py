

from typing import Union
import base64

from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

from src.engine.cryptography_center.encryption_strategy import EncryptionStrategy


class Cipher:
    def __init__(self, strategy: EncryptionStrategy):
        self.strategy = strategy

    def encrypt(self, data: Union[str, bytes]) -> str:
        if isinstance(data, str):
            data = data.encode()
        encrypted_data = self.strategy.encrypt(data)
        return base64.b64encode(encrypted_data).decode()

    def decrypt(self, data: str) -> Union[str, bytes]:
        encrypted_data = base64.b64decode(data)
        decrypted_data = self.strategy.decrypt(encrypted_data)
        try:
            return decrypted_data.decode()
        except UnicodeDecodeError:
            return decrypted_data

    def encrypt_file(self, file_path: str, output_path: str):
        with open(file_path, 'rb') as file:
            data = file.read()
        encrypted_data = self.strategy.encrypt(data)
        with open(output_path, 'wb') as file:
            file.write(encrypted_data)

    def decrypt_file(self, file_path: str, output_path: str):
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = self.strategy.decrypt(encrypted_data)
        with open(output_path, 'wb') as file:
            file.write(decrypted_data)

    @staticmethod
    def create_hash(data: str) -> str:
        hash_obj = SHA256.new(data.encode())
        return base64.b64encode(hash_obj.digest()).decode()

    @staticmethod
    def check_hash(data: str, given_hash: str) -> bool:
        return Cipher.create_hash(data) == given_hash

    @staticmethod
    def generate_key(key_size: int = 32) -> bytes:
        return get_random_bytes(key_size)

    @staticmethod
    def generate_password(length: int = 16) -> str:
        return base64.b64encode(get_random_bytes(length)).decode()[:length]

    @staticmethod
    def base64_encode(data: bytes) -> str:
        return base64.b64encode(data).decode()

    @staticmethod
    def base64_decode(data: str) -> bytes:
        return base64.b64decode(data)

    @staticmethod
    def save_to_file(filename: str, data: bytes):
        with open(filename, 'wb') as file:
            file.write(data)

    @staticmethod
    def read_from_file(filename: str) -> bytes:
        with open(filename, 'rb') as file:
            return file.read()

    @staticmethod
    def generate_rsa_keypair(key_size: int = 2048):
        key = RSA.generate(key_size)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key


# Example usage
if __name__ == '__main__':
    from src.engine.cryptography_center.encryption_strategy import AESEncryptionStrategy, RSAEncryptionStrategy

    # AES Example
    aes_encryption_key = Cipher.generate_key(32)  # 256-bit key
    aes_encryption_strategy = AESEncryptionStrategy(aes_encryption_key)
    aes_cipher = Cipher(aes_encryption_strategy)

    aes_encrypted = aes_cipher.encrypt('Hello, World!')
    aes_decrypted = aes_cipher.decrypt(aes_encrypted)
    print(f'Encrypted (AES): {aes_encrypted}')
    print(f'Decrypted (AES): {aes_decrypted}')

    # RSA Example
    rsa_private_key, rsa_public_key = Cipher.generate_rsa_keypair()
    rsa_public_key_obj = RSA.import_key(rsa_public_key)
    rsa_private_key_obj = RSA.import_key(rsa_private_key)
    rsa_encryption_strategy = RSAEncryptionStrategy(rsa_public_key_obj, rsa_private_key_obj)
    rsa_cipher = Cipher(rsa_encryption_strategy)

    rsa_encrypted = rsa_cipher.encrypt('Hello, RSA!')
    rsa_decrypted = rsa_cipher.decrypt(rsa_encrypted)
    print(f'Encrypted (RSA): {rsa_encrypted}')
    print(f'Decrypted (RSA): {rsa_decrypted}')

    # Hash Example
    hash_result = Cipher.create_hash('Hello, World!')
    print(f'Hash: {hash_result}')
    print(f'Check Hash: {Cipher.check_hash("Hello, World!", hash_result)}')

    # File encryption example
    file_data = b'This is some data to encrypt and save to a file.'
    aes_cipher.encrypt_file('example.txt', 'encrypted_file.dat')
    aes_cipher.decrypt_file('encrypted_file.dat', 'decrypted_file.txt')

    with open('decrypted_file.txt', 'rb') as file_handle:
        decrypted_file_content = file_handle.read()
    print(f'Decrypted File Data: {decrypted_file_content.decode()}')

    # Random password generation
    print(f'Random Password: {Cipher.generate_password(16)}')
