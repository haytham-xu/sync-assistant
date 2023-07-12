
from support.encrypter import encrypter
from support import filefolder

class FileModel:
    __code = None
    __fs_id = None
    __file_name = None
    __middle_path = None
    __local_base_path = None
    __cloud_base_path = None
    __source_md5 = None
    __encrypt_md5 = None
    __encrypt = None
    __delete = None
    __delete_time = None
    __local_mtime = None
    __db_mtime = None
    __is_dir = None

    def get_code(self):
        return self.__code
    def get_fs_id(self):
        return self.__fs_id
    def get_file_name(self):
        return self.__file_name
    def get_middle_path(self):
        return self.__middle_path
    def get_local_base_path(self):
        return self.__local_base_path
    def get_cloud_base_path(self):
        return self.__cloud_base_path
    def get_source_md5(self):
        return self.__source_md5
    def get_encrypt_md5(self):
        return self.__encrypt_md5
    def get_encrypt(self):
        return self.__encrypt
    def get_delete(self):
        return self.__delete
    def get_delete_time(self):
        return self.__delete_time
    def get_local_mtime(self):
        return self.__local_mtime
    def get_db_mtime(self):
        return self.__db_mtime
    def get_is_dir(self):
        return self.__is_dir


    def set_code(self, code):
        self.__code = code
    def set_fs_id(self, fs_id):
        self.__fs_id = fs_id
    def set_file_name(self, file_name):
        self.__file_name = file_name
    def set_middle_path(self, middle_path):
        self.__middle_path = middle_path
    def set_local_base_path(self, local_base_path):
        self.__local_base_path = local_base_path
    def set_cloud_base_path(self, cloud_base_path):
        self.__cloud_base_path = cloud_base_path
    def set_source_md5(self, source_md5):
        self.__source_md5 = source_md5
    def set_encrypt_md5(self, encrypt_md5):
        self.__encrypt_md5 = encrypt_md5
    def set_encrypt(self, encrypt):
        self.__encrypt = encrypt
    def set_delete(self, delete):
        self.__delete = delete
    def set_delete_time(self, delete_time):
        self.__delete_time = delete_time
    def set_local_mtime(self, local_mtime):
        self.__local_mtime = local_mtime
    def set_db_mtime(self, db_mtime):
        self.__db_mtime = db_mtime
    def set_is_dir(self, is_dir):
        self.__is_dir = is_dir

    def to_json(self):
        return {
            "code": self.__code,
            "fs_id": self.__fs_id,
    		"file_name": self.__file_name,
    		"middle_path": self.__middle_path,
    		"local_base_path": self.__local_base_path,
    		"cloud_base_path": self.__cloud_base_path,
    		"source_md5": self.__source_md5,
    		"encrypt_md5": self.__encrypt_md5,
    		"encrypt": self.__encrypt,
    		"delete": self.__delete,
    		"delete_time": self.__delete_time,
    		"local_mtime": self.__local_mtime,
    		"db_mtime": self.__db_mtime,
            "is_dir": self.__is_dir,
        }

def create_quick_index(base_path:str, file_path:str):
    if base_path[-1] != '/':
        base_path += '/'
    file_name = file_path.split('/')[-1]
    middle_path = file_path.removeprefix(base_path)
    file_code = encrypter.string_hash(middle_path)
    is_dir = filefolder.is_folder(file_path)
    local_mtime = None
    if not is_dir:
        local_mtime = filefolder.get_mtime(file_path)

    new_file_model = FileModel()
    new_file_model.set_code(file_code)
    new_file_model.set_file_name(file_name)
    new_file_model.set_middle_path(middle_path)
    new_file_model.set_local_mtime(local_mtime)
    new_file_model.set_is_dir(is_dir)
    return new_file_model
