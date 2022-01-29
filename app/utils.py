# this file contains all the utility functions

from passlib.context import CryptContext
from cryptography.fernet import Fernet

from app.config import environment_variable

import logging

logger = logging.getLogger(__name__)

CIPHER_KEY = environment_variable.CIPHER_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hash user's password
def hash_password(password):
    logger.info("hashing function called")
    return pwd_context.hash(password)

# validates hash for user login
def verify_password(plain_password, hashed_password):
    logger.info("verify hash function called")
    return pwd_context.verify(plain_password, hashed_password)

# encrypt password
def encrypt_password(plain_password, encryption_key = CIPHER_KEY):
    
    logger.info("encryption function called")
    byte_plain_password = bytes(plain_password, 'utf-8')
    encrypted_password = Fernet(encryption_key).encrypt(byte_plain_password)
    str_encrypted_password = encrypted_password.decode('utf-8')

    return str_encrypted_password

# decrypt password
def decrypt_password(str_encrypted_password, encryption_key = CIPHER_KEY):
    
    logger.info("decryption function called")
    byte_encrypted_password = bytes(str_encrypted_password, 'utf-8')
    plain_password = Fernet(encryption_key).decrypt(byte_encrypted_password)

    return plain_password