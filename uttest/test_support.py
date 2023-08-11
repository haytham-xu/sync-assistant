
from repository import repository
from model import file_model, context_model
from service import cloud_file_service
from support import path_support, encrypter_support
from uttest import test_constant

def local_create_store_file(middle_path:str, file_content:str, file_db:repository.FileDB, encrypt:bool, local_mtime:str):
    folder_context:context_model.FolderContext = file_db.get_folder_context()
    local_file_path = file_db.get_folder_context().get_local_base_path() + middle_path
    path_support.create_file(local_file_path, file_content)
    a_file_model = file_model.build_from_file(folder_context, local_file_path, "", encrypt)
    file_db.add_update_file_by_model(a_file_model)
    file_db.update_file_model_local_mtime_by_code(a_file_model.get_code(), local_mtime)

def upload_mock_cloud_to_cloud(mock_cloud_db:repository.FileDB, target_cloud_db_path:str):
    file_model_dict:dict = mock_cloud_db.get_file_dict()
    for file_code in file_model_dict.keys():
        a_file_model:file_model.FileModel = file_model_dict[file_code]
        cloud_file_service.upload_unencryot_file(a_file_model.get_file_local_path(), a_file_model.get_file_cloud_path())
    cloud_file_service.upload_unencryot_file(mock_cloud_db.get_db_context().get_local_db_path(), target_cloud_db_path)

def clean_test_environment():
    path_support.remove_path(test_constant.BASE_PATH_LOCAL_ROOT)
    cloud_file_service.delete_file_or_folder(test_constant.CLOUD_PATH_ROOT)

def build_index(middle_path:str, local_mtime:str, encrypt:bool):
    file_code = encrypter_support.string_hash(middle_path)
    file_name = middle_path.split("/")[-1]
    return {
        file_model.KEY_CODE: file_code,
        file_model.KEY_FILE_NAME: file_name,
        file_model.KEY_MIDDLE_PATH: middle_path,
        file_model.KEY_LOCAL_MTIME: local_mtime,
        file_model.KEY_ENCRYPT: encrypt
    }

def build_indexs(index_list:list):
    latest_index = {}
    for a_index in index_list:
        latest_index[a_index[file_model.KEY_CODE]] = a_index
    return latest_index
