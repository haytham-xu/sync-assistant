
'''
    {
        'category': 6, 
        'fs_id': 704xxxx0635, 
        'isdir': 0, 
        'local_ctime': 16xx311, 
        'local_mtime': 16xx3400,
        'md5': '15aeacxxxxx01f8b', 
        'path': '/apxxxxx_file.md', 
        'server_ctime': 168xx39, 
        'server_filename': 'same_file.md', 
        'encrypt': 16xx539, 
        'size': 7
    }
'''
class CloudFileModel:
    __category = None
    __fs_id = None
    __is_dir = None
    __local_ctime = None
    __local_mtime = None
    __md5 = None
    __path = None
    __server_ctime = None
    __server_filename = None
    __server_mtime = None
    __encrypt = None
    __size = None

    def get_category(self):
        return self.__category
    def get_fs_id(self):
        return self.__fs_id
    def get_is_dir(self):
        return self.__is_dir    
    def get_local_ctime(self):
        return self.__local_ctime
    def get_local_mtime(self):
        return self.__local_mtime
    def get_md5(self):
        return self.__md5
    def get_path(self):
        return self.__path
    def get_server_ctime(self):
        return self.__server_ctime
    def get_server_filename(self):
        return self.__server_filename
    def get_encrypt(self):
        return self.__encrypt
    def get_size(self):
        return self.__size
    def get_server_mtime(self):
        return self.__server_mtime

    def set_category(self, category):
        self.__category = category
    def set_fs_id(self, fs_id):
        self.__fs_id = fs_id
    def set_is_dir(self, is_dir):
        self.__is_dir = is_dir
    def set_local_ctime(self, local_ctime):
        self.__local_ctime = local_ctime
    def set_local_mtime(self, local_mtime):
        self.__local_mtime = local_mtime
    def set_md5(self, md5):
        self.__md5 = md5
    def set_path(self, path):
        self.__path = path
    def set_server_ctime(self, server_ctime):
        self.__server_ctime = server_ctime
    def set_server_filename(self, server_filename):
        self.__server_filename = server_filename
    def set_encrypt(self, encrypt):
        self.__encrypt = encrypt
    def set_size(self, size):
        self.__size = size
    def set_server_mtime(self, server_mtime):
        self.__server_mtime = server_mtime
    


    def to_json(self):
        return {
            "category": self.__category,
            "fs_id": self.__fs_id,
    		"local_ctime": self.__local_ctime,
    		"local_mtime": self.__local_mtime,
    		"md5": self.__md5,
    		"path": self.__path,
    		"server_ctime": self.__server_ctime,
    		"server_filename": self.__server_filename,
            "server_mtime": self.__server_mtime,
    		"encrypt": self.__encrypt,
    		"size": self.__size,
            "is_dir": self.__is_dir,
        }