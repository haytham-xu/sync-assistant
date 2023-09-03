
from model import context_model

KEY_FOLDER_CONTEXT = 'folder_context'
KEY_CODE = 'code'
KEY_FS_ID = 'fs_id'
KEY_FILE_NAME = 'file_name'
KEY_MIDDLE_PATH = 'middle_path'
KEY_ENCRYPT_MIDDLE_PATH= 'encrypt_middle_path'
KEY_ENCRYPT = 'encrypt'
KEY_MTIME = 'mtime'


class BaseFileModel:

    __folder_context: context_model.FolderContext
    __code: str
    __fs_id: str
    __file_name: str
    __middle_path: str
    __encrypt: bool
    __mtime: str
    
    def __init__(self, folder_context:context_model.FolderContext, code:str, fs_id:str, file_name:str, middle_path:str, encrypt:bool, mtime:str):
        self.__folder_context = folder_context
        self.__code = code
        self.__fs_id = fs_id
        self.__file_name = file_name
        self.__middle_path = middle_path
        self.__encrypt = encrypt
        self.__mtime = mtime

    def to_json(self):
        return {
            KEY_FOLDER_CONTEXT: self.__folder_context.to_json(),
            KEY_CODE: self.__code,
            KEY_FS_ID: self.__fs_id,
            KEY_FILE_NAME: self.__file_name,
            KEY_MIDDLE_PATH: self.__middle_path,
            KEY_ENCRYPT: self.__encrypt,
            KEY_MTIME: self.__mtime,
        }
    
    def get_folder_context(self):
        return self.__folder_context
    def set_folder_context(self, folder_context:context_model.FolderContext):
        self.__folder_context = folder_context

    def get_code(self):
        return self.__code
    def set_code(self, code:str):
        self.__code = code

    def get_fs_id(self):
        return self.__fs_id
    def set_fs_id(self, fs_id:str):
        self.__fs_id = fs_id

    def get_file_name(self):
        return self.__file_name
    def set_file_name(self, file_name:str):
        self.__file_name = file_name
    
    def get_middle_path(self):
        return self.__middle_path
    def set_middle_path(self, middle_path:str):
        self.__middle_path = middle_path

    def get_encrypt(self):
        return self.__encrypt
    def set_encrypt(self, encrypt:bool):
        self.__encrypt = encrypt
    
    def get_mtime(self):
        return self.__mtime
    def set_mtime(self, local_mtime:str):
        self.__mtime = local_mtime
