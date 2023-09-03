
from support import path_support

LOCAL_BASE_PATH_KEY = 'local_base_path'
CLOUD_BASE_PATH_KEY = 'cloud_base_path'
SWAP_BASE_PATH_KEY = 'swap_base_path'

class FolderContext:
    __local_base_path:str
    __cloud_base_path:str
    __swap_base_path:str
    def __init__(self, local_base_path, cloud_base_path, swap_base_path):
        # self.__local_base_path = path_support.format_folder_path(local_base_path)
        # self.__cloud_base_path = path_support.format_folder_path(cloud_base_path)
        # self.__swap_base_path = path_support.format_folder_path(swap_base_path)
        self.__local_base_path = local_base_path
        self.__cloud_base_path = cloud_base_path
        self.__swap_base_path = swap_base_path
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

def get_local_db_name(the_folder_context: FolderContext):
    local_base_path = the_folder_context.get_local_base_path()
    folder_name = path_support.get_file_folder_name(local_base_path)
    return '.' + folder_name + '.json'

def get_cloud_db_name(the_folder_context: FolderContext):
    cloud_base_path = the_folder_context.get_cloud_base_path()
    folder_name = path_support.get_file_folder_name(cloud_base_path)
    return '.' + folder_name + '.json'


def get_local_db_path(the_folder_context: FolderContext):
    return path_support.merge_path([the_folder_context.get_local_base_path(), get_local_db_name(the_folder_context)])

def get_cloud_db_path(the_folder_context: FolderContext):
    return path_support.merge_path([the_folder_context.get_cloud_base_path(), get_cloud_db_name(the_folder_context)])

def get_swap_db_path(the_folder_context: FolderContext):
    return path_support.merge_path([the_folder_context.get_swap_base_path(), get_cloud_db_name(the_folder_context)])
