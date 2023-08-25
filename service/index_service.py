
import os
from support import path_support, encrypter_support
from model import base_file_model
from support.path_support import merge_path

def get_latest_index(base_path:str, encrypt: bool):
    file_list = []
    for cur_path, _, files in os.walk(base_path):
        for file_name in files:
            if file_name[0] == '.':
                continue
            file_path = merge_path([cur_path, file_name])
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
