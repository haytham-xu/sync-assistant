
from support import file_support

import os
import shutil

def create_file(file_path, file_content):
    parent_path = '/'.join(file_path.split('/')[:-1])
    create_folder(parent_path)
    file_support.write_file(file_path, file_content)

def create_file_byte(file_path, file_content):
    parent_path = '/'.join(file_path.split('/')[:-1])
    create_folder(parent_path)
    file_support.write_file_byte(file_path, file_content)

def create_folder(folder_path):
    if not is_exist(folder_path):
        os.makedirs(folder_path)

def remove_path(path):
    if is_exist(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

def is_exist(file_folder_path):
    return os.path.exists(file_folder_path) 

def is_exist(path):
    return os.path.exists(path)

def is_folder(path):
    return os.path.isdir(path)

def list_folder(path:str):
    folder_list = []
    for file_or_folder in os.listdir(path):
        file_or_folder_path = path + file_or_folder
        if is_folder(file_or_folder_path):
            folder_list.append(file_or_folder_path + '/')
    return folder_list

ignore_file_folder_list = ['.DS_Store']

def list_file(path:str):
    file_list = []
    for file_or_folder in os.listdir(path):
        if file_or_folder in ignore_file_folder_list:
            continue
        file_or_folder_path = path  + file_or_folder
        if not is_folder(file_or_folder_path):
            file_list.append(file_or_folder_path)
    return file_list

def list_folder_file(path:str):
    if not is_exist(path):
        return [], []
    return list_folder(path), list_file(path)

def get_mtime(path):
    return int(os.stat(path).st_mtime)


def format_folder_path(path:str):
    if path[-1] != '/':
        path += '/'
    return path

def merge_path(path_list:list):
    output_path = ""
    for p in path_list:
        output_path = os.path.join(output_path, p)    
    return output_path

def format_middle_path(middle_path:str):
    if middle_path.startswith("/"):
        return middle_path[1:]
    return middle_path

def list_folders_files(path):
    return [fof for fof in os.listdir(path) if fof not in ignore_file_folder_list]

def list_file_recursion(current_path:str):
    folder_file_list = list_folders_files(current_path)
    file_list = []
    for folder_or_file in folder_file_list:
        folder_or_file_path:str = merge_path([current_path, folder_or_file])
        if is_folder(folder_or_file_path):
            file_list += list_file_recursion(folder_or_file_path)
        else:
            file_list.append(folder_or_file_path)
    return file_list

'''
|       | a     | /a    | a/    | /a/   |       | .a    | /.a   | .a/   | /.a/  |       | a.md  | /a.md | a.md/ | /a.md/|
|  ---  |  ---  |  ---  |  ---  |  ---  |  ---  |  ---  |  ---  |  ---  |  ---  |  ---  |  ---  |  ---  |  ---  |  ---  |
| first | a/    | /a/   | a/    | /a/   |       | .a/   | /.a/  | .a/   | /.a/  |       | ?     | ?     | ?     | ?     |
| middle| a/    | a/    | a/    | a/    |       | .a/   | .a/   | .a/   |  .a/  |       | ?     | ?     | ?     | ?     |
| last  | a     | a     | a     | a     |       | .a    | .a    | .a    | .a    |       | a.md  | a.md  | a.md  | a.md  |
'''
