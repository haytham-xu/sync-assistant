
from model.context_model import FolderContext

KEY_FOLDER_CONTEXT = 'folder_context'
KEY_CODE = 'code'
KEY_FS_ID = 'fs_id'
KEY_FILE_NAME = 'file_name'
KEY_MIDDLE_PATH = 'middle_path'
KEY_ENCRYPT_MIDDLE_PATH= 'encrypt_middle_path'
KEY_ENCRYPT = 'encrypt'
KEY_MTIME = 'mtime'

class BaseFileModel:

    __folder_context:FolderContext
    __code:str
    __fs_id:str
    __file_name:str
    __middle_path:str
    __encrypt:bool
    __mtime:str
    
    def __init__(self, folder_context:FolderContext, code:str, fs_id:str, file_name:str, middle_path:str, encrypt:bool, mtime:str):
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
    def set_folder_context(self, folder_context:FolderContext):
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


    # '''
    # local_mode unencrypted -->  middle is unencrypted, just return
    # local_mode encrypted   -->  middle is unencrypted, just return
    # cloud_mode unencrypted -->  middle is unencrypted, just return
    # cloud_mode encrypted   -->  middle is encrypted, unencrypt then return
    # '''
    # def get_file_local_path(self):
    #     if self.get_encrypt() and self.get_mode() == MODE_CLOUD:
    #         unencrypted_middle_path = '/'.join([encrypter_support.string_base64_to_source_string(p) for p in self.get_middle_path().split('/')])
    #         return path_support.merge_path([self.__folder_context.get_local_base_path(), unencrypted_middle_path])
    #     return path_support.merge_path([self.__folder_context.get_local_base_path(), self.get_middle_path()])
    # '''
    # local_mode unencrypted -->  middle is unencrypted, just return
    # local_mode encrypted   -->  middle is unencrypted, should encrypted then return
    # cloud_mode unencrypted -->  middle is unencrypted, just return
    # cloud_mode encrypted   -->  middle is encrypted, just return
    # '''
    # def get_file_cloud_path(self):
    #     if self.get_encrypt() and self.get_mode() == MODE_LOCAL:
    #         encrypted_middle_path = '/'.join([encrypter_support.string_source_to_base64_string(p) for p in self.get_middle_path().split('/')])
    #         return path_support.merge_path([self.__folder_context.get_cloud_base_path(), encrypted_middle_path])
    #     return path_support.merge_path([self.__folder_context.get_cloud_base_path(), self.get_middle_path()])

    # '''
    # local_mode unencrypted -->  middle is unencrypted, just return
    # local_mode encrypted   -->  middle is unencrypted, should encrypted then return
    # cloud_mode unencrypted -->  middle is unencrypted, just return
    # cloud_mode encrypted   -->  middle is encrypted, just return
    # swap is always for encrypted mode, so the file and folder here should always be encrypted.
    # '''
    # def get_file_swap_path(self):
    #     if self.get_encrypt() and self.get_mode() == MODE_LOCAL:
    #         encrypted_middle_path = '/'.join([encrypter_support.string_source_to_base64_string(p) for p in self.get_middle_path().split('/')])
    #         return path_support.merge_path([self.__folder_context.get_swap_base_path(), encrypted_middle_path])
    #     return path_support.merge_path([self.__folder_context.get_swap_base_path(), self.get_middle_path()])
    