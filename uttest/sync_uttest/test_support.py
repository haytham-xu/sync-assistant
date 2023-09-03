
from service import cloud_file_service
from repository import local_repository
from repository import cloud_repository
from model import context_model
from model import base_file_model
from model import local_file_model
from model import cloud_file_model
from support import path_support, encrypter_support
from uttest.sync_uttest import test_constant


def local_create_store_file(unencrypted_middle_path: str, file_content: str, local_file_db: local_repository.LocalRepository, encrypt: bool, local_mtime: str):
    folder_context: context_model.FolderContext = local_file_db.get_folder_context()
    local_file_path = path_support.merge_path([folder_context.get_local_base_path(), unencrypted_middle_path])
    print(local_file_path)
    path_support.create_override_file(local_file_path, file_content)
    a_local_file_model: local_file_model.LocalFileModel = local_file_model.build_from_file_path(folder_context, local_file_path, local_mtime, encrypt)
    local_file_db.add_file_model_from_local_file_model(a_local_file_model)


def cloud_create_store_file(unencrypt_middle_path: str, file_content: str, cloud_file_db: cloud_repository.CloudRepository, encrypt: bool, mtime: str):
    folder_context:context_model.FolderContext = cloud_file_db.get_folder_context()
    middle_path = ""
    temp_local_path = ""
    code = encrypter_support.string_hash(unencrypt_middle_path)
    file_name = path_support.get_file_folder_name(unencrypt_middle_path)

    local_unencrypt_file_path = path_support.merge_path([test_constant.MOCK_CLOUD_PATH_ROOT, unencrypt_middle_path])
    path_support.create_override_file(local_unencrypt_file_path, file_content)


    if encrypt:
        middle_path = path_support.merge_path([encrypter_support.string_source_to_base64_string(p) for p in path_support.get_path_components(unencrypt_middle_path)])
        file_name = encrypter_support.string_source_to_base64_string(file_name)
        local_encrypt_file_path = path_support.merge_path([test_constant.MOCK_CLOUD_PATH_ROOT, middle_path])
        encrypter_support.file_encrypt(local_unencrypt_file_path, local_encrypt_file_path)
        temp_local_path = local_encrypt_file_path
    else:
        middle_path = unencrypt_middle_path
        temp_local_path = local_unencrypt_file_path
    a_cloud_file_model: cloud_file_model.CloudFileModel = cloud_file_model.CloudFileModel(folder_context, code, None, file_name, middle_path, encrypt, mtime)
    cloud_file_db.add_file_model_from_cloud_file_model(a_cloud_file_model)
    
    temp_cloud_path = a_cloud_file_model.get_cloud_file_path()
    cloud_file_service.upload_file_by_path(temp_local_path, temp_cloud_path)

def clean_test_environment():
    path_support.remove_path(test_constant.BASE_PATH_LOCAL_ROOT)
    cloud_file_service.delete_file_or_folder(test_constant.CLOUD_PATH_ROOT)

def build_index(middle_path:str, mtime:str, encrypt:bool):
    file_code = encrypter_support.string_hash(middle_path)
    file_name = path_support.get_file_folder_name(middle_path)
    return {
        base_file_model.KEY_CODE: file_code,
        base_file_model.KEY_FILE_NAME: file_name,
        base_file_model.KEY_MIDDLE_PATH: middle_path,
        base_file_model.KEY_MTIME: mtime,
        base_file_model.KEY_ENCRYPT: encrypt
    }

def build_indexs(index_list:list):
    latest_index = {}
    for a_index in index_list:
        latest_index[a_index[base_file_model.KEY_CODE]] = a_index
    return latest_index
