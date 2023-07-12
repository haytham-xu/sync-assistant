
import os
from model import file_model
from support import baiduwangpan
from service import cloud_file_service

def get_cloud_base_index(path:str, inlcude_folder: bool = False):
    file_folder_set = cloud_file_service.list_folder_file_recursion(path)
    # todo

def get_local_index_base(base_path:str, inlcude_folder: bool = False):
    ff_list = []
    for cur_path, folders, files in os.walk(base_path):
        if inlcude_folder:
            for f in folders:
                ff_list.append(file_model.create_quick_index(base_path, cur_path + '/' + f))
        for f in files:
            ff_list.append(file_model.create_quick_index(base_path, cur_path + '/' + f))
    result = {}
    for f in ff_list:
        result[f.get_code()] = f
    return result
