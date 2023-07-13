
import os, shutil, enum

def create_file(file_path, file_content):
    parent_path = '/'.join(file_path.split('/')[:-1])
    create_folder(parent_path)
    write_file(file_path, file_content)

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

class ReadMode(enum.Enum):
    STEAM = ""
    STRING = "read()"
    STRING_LIST = "readlines()"    

def read_file(file_path, mode='r', read_mode=ReadMode.STRING):
    try:
        res = None
        with open(file_path, mode) as f:
            if read_mode == ReadMode.STEAM:
                res = f
            elif read_mode == ReadMode.STRING:
                res = f.read()
            else:
                res = f.readlines()                    
        return res
    except Exception as err:
        raise Exception("Read file failed: ", err)
    finally:
        f.close()

def append_file(file_path, content, mode='a'):
    try:
        with open(file_path, mode) as f:
            f.write(content)
    except Exception as err:
        raise Exception("Append file failed: ", err)
    finally:
        f.close()

def write_file(file_path:str, content, mode='w'):
    parent_path = '/'.join(file_path.split('/')[:-1])
    create_folder(parent_path)
    try:
        with open(file_path, mode) as f:
            f.write(content)
    except Exception as err:
        raise Exception("Write file failed: ", err)
    finally:
        f.close()

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

def list_file(path:str):
    file_list = []
    for file_or_folder in os.listdir(path):
        if file_or_folder in ['.DS_Store']:
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
