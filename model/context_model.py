
from support import path_support

LOCAL_BASE_PATH_KEY = 'local_base_path'
CLOUD_BASE_PATH_KEY = 'cloud_base_path'
SWAP_BASE_PATH_KEY = 'swap_base_path'

class FolderContext:
    __local_base_path:str
    __cloud_base_path:str
    __swap_base_path:str
    def __init__(self, local_base_path, cloud_base_path, swap_base_path):
        self.__local_base_path = path_support.format_folder_path(local_base_path)
        self.__cloud_base_path = path_support.format_folder_path(cloud_base_path)
        self.__swap_base_path = path_support.format_folder_path(swap_base_path)
    def get_local_base_path(self):
        return self.__local_base_path
    def get_cloud_base_path(self):
        return self.__cloud_base_path
    def get_swap_base_path(self):
        return self.__swap_base_path
    def set_local_base_path(self, local_base_path):
        self.__local_base_path = local_base_path
    def set_cloud_base_path(self, cloud_base_path):
        self.__cloud_base_path = cloud_base_path
    def set_swap_base_path(self, swap_base_path):
        self.__swap_base_path = swap_base_path
    def to_json(self):
        return {
            LOCAL_BASE_PATH_KEY: self.__local_base_path,
            CLOUD_BASE_PATH_KEY: self.__cloud_base_path,
            SWAP_BASE_PATH_KEY: self.__swap_base_path
        }

class DBContext:
    __folder_context: FolderContext
    __db_name:str
    __local_db_path:str
    __cloud_db_path:str
    __swap_db_path:str
    def __init__(self, local_base_path, cloud_base_path, swap_base_path):
        self.__folder_context = FolderContext(local_base_path, cloud_base_path, swap_base_path)
        folder_name = local_base_path.split('/')[-1]
        self.__db_name = '.' + folder_name + '.json'
        self.__local_db_path = self.__folder_context.get_local_base_path() + self.__db_name
        self.__cloud_db_path = self.__folder_context.get_cloud_base_path() + self.__db_name
        self.__swap_db_path = self.__folder_context.get_swap_base_path() + self.__db_name
    def get_db_name(self):
        return self.__db_name
    def get_local_db_path(self):
        return self.__local_db_path
    def get_cloud_db_path(self):
        return self.__cloud_db_path
    def get_swap_db_path(self):
        return self.__swap_db_path
    def set_db_name(self, db_name):
        self.__db_name = db_name
    def set_local_db_path(self, local_db_path):
        self.__local_db_path = local_db_path
    def set_cloud_db_path(self, cloud_db_path):
        self.__cloud_db_path = cloud_db_path
    def set_swap_db_path(self, swap_db_path):
        self.__swap_db_path = swap_db_path
