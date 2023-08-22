
import hashlib, base64

from support.config_support import config
from cryptography.fernet import Fernet
from support import path_support, file_support

BUF_SIZE = 65536
fernet = Fernet(config.get_encrypt_key().encode())

def string_encrypt(string: str):
    return fernet.encrypt(string.encode())

def string_decrypt(string:str):
    return fernet.decrypt(string).decode()

def string_hash(string:str): # sha256
    sha256 = hashlib.sha256()
    sha256.update(string.encode())
    return sha256.hexdigest()

def file_encrypt(source_filepath, target_filepath):
    # file_data = file_support.read_file(source_filepath, 'rb', file_support.ReadMode.STRING)
    to_encrypted_data = file_support.read_file_as_byte_string(source_filepath)
    encrypted_data = fernet.encrypt(to_encrypted_data)
    # path_support.write_file(target_filepath, encrypted_data, 'wb')
    # file_support.write_file_byte(target_filepath, encrypted_data)
    path_support.create_file_byte(target_filepath, encrypted_data)

def file_decrtpt(source_filepath, target_filepath):
    # encrypted_data = file_support.read_file(source_filepath, 'rb', path_support.ReadMode.STRING)
    to_decrypted_data = file_support.read_file_as_byte_string(source_filepath)
    decrypted_data = fernet.decrypt(to_decrypted_data)
    # path_support.write_file(target_filepath, decrypted_data, 'wb')
    # file_support.write_file_byte(target_filepath, decrypted_data)
    path_support.create_file_byte(target_filepath, decrypted_data)

def get_sha256(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

def get_md5(file_path):
    md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)
    return md5.hexdigest()

def string_source_to_base64_string(source:str):
    return str(base64.b64encode(source.encode(encoding="utf-8")) , encoding = "utf-8")

def string_base64_to_source_string(base_str:str):
    return str(base64.b64decode(bytes(base_str, encoding = "utf8")), encoding = "utf-8")
