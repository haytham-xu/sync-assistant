
from support.config import config
from support import filefolder, path_support
from service import file_service
from model import local_file_model
import os

def get_db_config(base_path:str):
    base_path = path_support.format_folder_path(base_path)
    folder_name = base_path.split('/')[-1]
    db_name = '.' + folder_name + '.json'
    db_path = base_path + db_name
    return base_path, folder_name, db_name, db_path

def download_db_from_cloud(cloud_base_path: str):
    cloud_base_path, folder_name, db_name, _ = get_db_config(cloud_base_path)
    swap_base_path = config.get_swap_folder_path() + folder_name + '/'
    if file_service.is_file_exist_in_cloud(cloud_base_path + db_name):
        file_service.download_file(swap_base_path, cloud_base_path, db_name)
        return
    with open(swap_base_path + db_name, "w") as f:
        f.write("{}")
        f.close()

def read_cloud_db(cloud_base_path: str):
    download_db_from_cloud(cloud_base_path)
    cloud_base_path, folder_name, db_name, _ = get_db_config(cloud_base_path)
    swap_db_path = config.get_swap_folder_path() + folder_name + '/' + db_name
    db_json = filefolder.read_file(swap_db_path)
    res = {}
    for key, value in db_json.items():
        res[key] = local_file_model.create_file_model(value)
    return res
    
def read_local_db(local_base_path:str):
    local_base_path, _, _, db_path = get_db_config(local_base_path)
    if not os.path.exists(db_path):
        with open(db_path, "w") as f:
            f.write("{}")
            f.close()
    db_json = filefolder.read_file(db_path)
    res = {}
    for key, value in db_json.items():
        res[key] = local_file_model.create_file_model(value)
    return res

def upload_db_to_cloud(local_base_path, cloud_base_path):
    local_base_path, folder_name, db_name, local_db_path = get_db_config(local_base_path)
    swap_db_local_path = config.get_swap_folder_path() + folder_name + '/' + db_name
    swap_db_cloud_path = cloud_base_path + db_name
    file_service.upload_file(swap_db_local_path, swap_db_cloud_path)
