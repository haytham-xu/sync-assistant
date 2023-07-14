
from model.context_model import FolderContext
from support import encrypter_support, path_support

FOLDER_CONTEXT_KEY = 'folder_context'
FILE_CODE_KEY = 'code'
FS_ID_KEY = 'fs_id'
FILE_NAME_KEY = 'file_name'
MIDDLE_PATH_KEY = 'middle_path'
ENCRYPT_MIDDLE_PATH_KEY= 'encrypt_middle_path'
ENCRYPT_KEY = 'encrypt'
LOCAL_MTIME_KEY = 'local_mtime'

class FileModel:
    __folder_context:FolderContext
    __code:str
    __fs_id:str
    __file_name:str
    __middle_path:str
    __encrypt_middle_path:str
    __encrypt:bool
    __local_mtime:str
    def __init__(self, folder_context:FolderContext, local_file_path:str, fs_id:str='',encrypt:str=False):
        self.__folder_context = folder_context
        self.__file_name = local_file_path.split('/')[-1]
        self.__middle_path = local_file_path.removeprefix(folder_context.get_local_base_path())
        self.__encrypt_middle_path = '/'.join([encrypter_support.string_source_to_base64_string(p) for p in self.__middle_path.split('/')])
        self.__code = encrypter_support.string_hash(self.__middle_path)
        self.__encrypt = encrypt
        self.__local_mtime = path_support.get_mtime(local_file_path)
        self.__fs_id = fs_id        

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
            FOLDER_CONTEXT_KEY: self.__folder_context.to_json(),
            FILE_CODE_KEY: self.__code,
            FS_ID_KEY: self.__fs_id,
            FILE_NAME_KEY: self.__file_name,
            MIDDLE_PATH_KEY: self.__middle_path,
            ENCRYPT_KEY: self.__encrypt,
            LOCAL_MTIME_KEY: self.__local_mtime
        }

    def get_file_local_path(self):
        return self.__folder_context.get_local_base_path() + self.__middle_path
    def get_file_cloud_path(self):
        return self.__folder_context.get_cloud_base_path() + self.__middle_path
