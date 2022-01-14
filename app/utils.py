from passlib.context import CryptContext
from cryptography.fernet import Fernet

from .config import environment_variable

CIPHER_KEY = environment_variable.CIPHER_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def encrypt_password(plain_password, encryption_key = CIPHER_KEY):
    
    byte_plain_password = bytes(plain_password, 'utf-8')
    encrypted_password = Fernet(encryption_key).encrypt(byte_plain_password)
    str_encrypted_password = encrypted_password.decode('utf-8')

    return str_encrypted_password

def decrypt_password(str_encrypted_password, encryption_key = CIPHER_KEY):
    
    byte_encrypted_password = bytes(str_encrypted_password, 'utf-8')
    plain_password = Fernet(encryption_key).decrypt(byte_encrypted_password)

    return plain_password