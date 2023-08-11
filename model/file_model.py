
from model.context_model import FolderContext
from support import encrypter_support, path_support

KEY_FOLDER_CONTEXT = 'folder_context'
KEY_CODE = 'code'
KEY_FS_ID = 'fs_id'
KEY_FILE_NAME = 'file_name'
KEY_MIDDLE_PATH = 'middle_path'
KEY_ENCRYPT_MIDDLE_PATH= 'encrypt_middle_path'
KEY_ENCRYPT = 'encrypt'
KEY_LOCAL_MTIME = 'local_mtime'

class FileModel:
    __folder_context:FolderContext
    __code:str
    __fs_id:str
    __file_name:str
    __middle_path:str
    __encrypt_middle_path:str
    __encrypt:bool
    __local_mtime:str

    def get_folder_context(self):
        return self.__folder_context
    def get_code(self):
        return self.__code
    def get_fs_id(self):
        return self.__fs_id
    def get_file_name(self):
        return self.__file_name
    def get_middle_path(self):
        return self.__middle_path
    def get_encrypt_middle_path(self):
        return self.__encrypt_middle_path
    def get_encrypt(self):
        return self.__encrypt
    def get_local_mtime(self):
        return self.__local_mtime
    def set_folder_context(self, folder_context):
        self.__folder_context = folder_context
    def set_code(self, code):
        self.__code = code
    def set_fs_id(self, fs_id):
        self.__fs_id = fs_id
    def set_file_name(self, file_name):
        self.__file_name = file_name
    def set_middle_path(self, middle_path):
        self.__middle_path = middle_path
    def set_encrypt_middle_path(self, encrypt_middle_path):
        self.__encrypt_middle_path = encrypt_middle_path
    def set_encrypt(self, encrypt):
        self.__encrypt = encrypt
    def set_local_mtime(self, local_mtime):
        self.__local_mtime = local_mtime

    def to_json(self):
        return {
            KEY_FOLDER_CONTEXT: self.__folder_context.to_json(),
            KEY_CODE: self.__code,
            KEY_FS_ID: self.__fs_id,
            KEY_FILE_NAME: self.__file_name,
            KEY_MIDDLE_PATH: self.__middle_path,
            KEY_ENCRYPT: self.__encrypt,
            KEY_LOCAL_MTIME: self.__local_mtime
        }

    def get_file_local_path(self):
        return path_support.merge_path([self.__folder_context.get_local_base_path(), self.__middle_path])
    def get_file_cloud_path(self):
        return path_support.merge_path([self.__folder_context.get_cloud_base_path(), self.__middle_path])

def build_from_file(folder_context:FolderContext, local_file_path:str, fs_id:str='',encrypt:bool=False):
    the_file_model = FileModel()
    the_file_model.set_folder_context(folder_context)
    the_file_model.set_file_name(local_file_path.split('/')[-1])
    the_file_model.set_middle_path(local_file_path.removeprefix(folder_context.get_local_base_path()))
    the_file_model.set_encrypt_middle_path('/'.join([encrypter_support.string_source_to_base64_string(p) for p in the_file_model.get_middle_path().split('/')]))
    the_file_model.set_code(encrypter_support.string_hash(the_file_model.get_middle_path()))
    the_file_model.set_encrypt(encrypt)
    the_file_model.set_fs_id(fs_id)
    the_file_model.set_local_mtime(path_support.get_mtime(local_file_path))
    return the_file_model

def build_from_data(folder_context:FolderContext, code:str, fs_id:str, file_name:str, middle_path:str, encrypt:bool, local_mtime:str):
    the_file_model = FileModel()
    the_file_model.set_folder_context(folder_context)
    the_file_model.set_code(code)
    the_file_model.set_fs_id(fs_id)
    the_file_model.set_file_name(file_name)
    the_file_model.set_middle_path(middle_path)
    the_file_model.set_encrypt_middle_path('/'.join([encrypter_support.string_source_to_base64_string(p) for p in middle_path.split('/')]))
    the_file_model.set_encrypt(encrypt)
    the_file_model.set_local_mtime(local_mtime)
    return the_file_model
