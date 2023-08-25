
from model import context_model
from support import path_support
from support import bdwp_support
import shutil
import json

def create_buffer_folder(folder_context: context_model.FolderContext):
    path_support.create_folder(folder_context.get_swap_base_path())
    
def remove_buffer_folder(folder_context: context_model.FolderContext):
    shutil.rmtree(folder_context.get_swap_base_path())

def download_cloud_db(folder_context:context_model.FolderContext):
    cloud_db_name = context_model.get_cloud_db_name(folder_context)
    cloud_db_path = context_model.get_cloud_db_path(folder_context)
    swap_db_path = context_model.get_swap_db_path(folder_context)
    if bdwp_support.is_file_exist_in_cloud(cloud_db_path):
        bdwp_support.download_file_with_path(folder_context.get_swap_base_path(), folder_context.get_cloud_base_path(), cloud_db_name)
    else:
        path_support.create_file(swap_db_path, json.dumps({}))

def upload_cloud_db(folder_context:context_model.FolderContext):
    swap_db_path = context_model.get_swap_db_path(folder_context)
    cloud_db_path = context_model.get_cloud_db_path(folder_context)
    bdwp_support.upload_file(swap_db_path, cloud_db_path)
