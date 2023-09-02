
from support import path_support
from support import encrypter_support
from model import base_file_model
from support import path_support
from support import file_support

import os
import json

def get_latest_index(base_path:str, encrypt: bool):
    file_list = []
    for cur_path, _, files in os.walk(base_path):
        for file_name in files:
            if file_name[0] == '.':
                continue
            file_path = path_support.merge_path([cur_path, file_name])
            middle_path = path_support.format_middle_path(file_path.removeprefix(base_path))
            file_list.append({
                base_file_model.KEY_CODE: encrypter_support.string_hash(middle_path),
                base_file_model.KEY_MIDDLE_PATH: middle_path,
                base_file_model.KEY_ENCRYPT: encrypt,
                base_file_model.KEY_MTIME: path_support.get_mtime(file_path)
            })
    result = {}
    for a_file in file_list:
        result[a_file[base_file_model.KEY_CODE]] = a_file
    return result

def build_index_for_folder(folder_path:str, index_file_path:str):
    files_dict = {}
    files_path_list = path_support.list_file_recursion(folder_path)
    for a_file_path in files_path_list:
        file_name:str = os.path.split(a_file_path)[-1] # only filename
        if file_name.startswith("."):
            continue
        file_code = encrypter_support.string_hash(file_name)
        file_md5 = encrypter_support.get_md5(a_file_path)
        files_dict[file_code + '-' + file_md5] = a_file_path
        print("build index for: " + a_file_path)
    path_support.create_override_file(index_file_path, json.dumps(files_dict, indent=4, ensure_ascii=False))

def get_index_for_folder(folder_path:str, rebuild_index:bool):
    folder_name = os.path.split(folder_path)[-1]
    index_file_name = ".{}-index.json".format(folder_name)
    index_file_path = os.path.join(folder_path, index_file_name)
    if rebuild_index:
        build_index_for_folder(folder_path, index_file_path)
    res = file_support.read_file_as_string(index_file_path)
    return json.loads(res)
