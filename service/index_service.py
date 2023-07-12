
import os
from model import file_model
from service import cloud_file_service

def get_cloud_base_index(path:str, inlcude_folder: bool = False):
    file_folder_set = cloud_file_service.list_folder_file_recursion(path)
    ff_list = []
    for f in file_folder_set:
        if not inlcude_folder and f.get_is_dir():
            continue
        ff_list.append(file_model.create_cloud_quick_index(path, f))
    result = {}
    for f in ff_list:
        result[f.get_code()] = f.to_json()
    return result

def get_local_index_base(base_path:str, inlcude_folder: bool = False):
    ff_list = []
    for cur_path, folders, files in os.walk(base_path):
        if inlcude_folder:
            for f in folders:
                ff_list.append(file_model.create_local_quick_index(base_path, cur_path + '/' + f))
        for f in files:
            ff_list.append(file_model.create_local_quick_index(base_path, cur_path + '/' + f))
    result = {}
    for f in ff_list:
        result[f.get_code()] = f.to_json()
    return result
