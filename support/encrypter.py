
from support.config import config
from cryptography.fernet import Fernet
import hashlib, base64
from support import filefolder

BUF_SIZE = 65536

class Encrypter():
    def __init__(self):
        key = config.get_encrypt_key().encode()
        self.fernet = Fernet(key)
    def string_encrypt(self, string: str):
        return self.fernet.encrypt(string.encode())
    def string_decrypt(self, string:str):
        return self.fernet.decrypt(string).decode()
    def string_hash(self, string:str): # sha256
        sha256 = hashlib.sha256()
        sha256.update(string.encode())
        return sha256.hexdigest()
    def file_encrypt(self, source_filepath, target_filepath):
        file_data = filefolder.read_file(source_filepath, 'rb', filefolder.ReadMode.STRING)
        encrypted_data = self.fernet.encrypt(file_data)
        filefolder.write_file(target_filepath, encrypted_data, 'wb')
    def file_decrtpt(self, source_filepath, target_filepath):
        encrypted_data = filefolder.read_file(source_filepath, 'rb', filefolder.ReadMode.STRING)
        decrypted_data = self.fernet.decrypt(encrypted_data)
        filefolder.write_file(target_filepath, decrypted_data, 'wb')
    def get_sha256(self,file_path):
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    def get_md5(self,file_path):
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
        return md5.hexdigest()
    def string_source_to_base64_string(self, source:str):
        return str(base64.b64encode(source.encode(encoding="utf-8")) , encoding = "utf-8")
    def string_base64_to_source_string(self, base_str:str):
        return str(base64.b64decode(bytes(base_str, encoding = "utf8")), encoding = "utf-8")
    
encrypter = Encrypter()    
