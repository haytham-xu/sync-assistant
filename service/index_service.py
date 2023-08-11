
import os
from model import file_model
from support import path_support, encrypter_support

def get_latest_index(base_path:str, encrypt: bool):
    file_list = []
    for cur_path, _, files in os.walk(base_path):
        for file_name in files:
            if file_name[0] == '.':
                continue
            file_path = cur_path + '/' + file_name
            middle_path = path_support.format_middle_path(file_path.removeprefix(base_path))
            file_list.append({
                file_model.KEY_CODE: encrypter_support.string_hash(middle_path),
                file_model.KEY_FILE_NAME: file_name,
                file_model.KEY_MIDDLE_PATH: middle_path,
                file_model.KEY_LOCAL_MTIME: path_support.get_mtime(file_path),
                file_model.KEY_ENCRYPT: encrypt
            })
    result = {}
    for a_file in file_list:
        result[a_file[file_model.KEY_CODE]] = a_file
    return result
