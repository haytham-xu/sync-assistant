
import os
from model import file_model
from support import path_support, encrypter_support

def get_latest_index(base_path:str, encrypt: bool):
    file_list = []
    for cur_path, _, files in os.walk(base_path):
        for file_name in files:
            file_path = cur_path + '/' + file_name
            middle_path = file_path.removeprefix(base_path)
            file_list.append({
                file_model.FILE_CODE_KEY: encrypter_support.string_hash(middle_path),
                file_model.FILE_NAME_KEY: file_name,
                file_model.MIDDLE_PATH_KEY: middle_path,
                file_model.LOCAL_MTIME_KEY: path_support.get_mtime(file_path),
                file_model.ENCRYPT_KEY: encrypt
            })
    result = {}
    for a_file in file_list:
        result[a_file[file_model.FILE_CODE_KEY]] = a_file
    return result
