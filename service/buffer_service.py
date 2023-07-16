
from model import context_model
from support import path_support, bdwp_support
import shutil, json

def create_buffer_folder(folder_context: context_model.FolderContext):
    path_support.create_folder(folder_context.get_swap_base_path())
    
def remove_buffer_folder(folder_context: context_model.FolderContext):
    shutil.rmtree(folder_context.get_swap_base_path())

def download_cloud_db(folder_context:context_model.FolderContext, db_context:context_model.DBContext):
    if bdwp_support.is_file_exist_in_cloud(db_context.get_cloud_db_path()):
        bdwp_support.download_file_with_path(folder_context.get_swap_base_path(), folder_context.get_cloud_base_path(), db_context.get_db_name())
    else:
        path_support.create_file(db_context.get_swap_db_path(), json.dumps({}))

def upload_cloud_db(db_context:context_model.DBContext):
    bdwp_support.upload_file(db_context.get_local_db_path(), db_context.get_cloud_db_path())
