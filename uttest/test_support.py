
from repository import local_repository, cloud_repository
from model import context_model, base_file_model, local_file_model, cloud_file_model
from service import cloud_file_service
from support import path_support, encrypter_support
from uttest import test_constant

def local_create_store_file(unencrypt_middle_path:str, file_content:str, local_file_db:local_repository.LocalRepository, encrypt:bool, local_mtime:str):
    folder_context:context_model.FolderContext = local_file_db.get_folder_context()
    local_file_path = path_support.merge_path([folder_context.get_local_base_path(), unencrypt_middle_path])
    path_support.create_file(local_file_path, file_content)
    a_local_file_model: local_file_model.LocalFileModel = local_file_model.build_from_file_path(folder_context, local_file_path, local_mtime, encrypt)
    local_file_db.add_file_model_from_local_file_model(a_local_file_model)


    # folder_context:context_model.FolderContext = file_db.get_folder_context()
    # local_file_path = path_support.merge_path([file_db.get_folder_context().get_local_base_path(), middle_path])
    # path_support.create_file(local_file_path, file_content)
    # a_file_model:file_model.FileModel = build_from_file_with_mtime(folder_context, local_file_path, mode, "", encrypt, local_mtime)
    # if encrypt and mode == file_model.MODE_CLOUD:
    #     mock_local_encrypted_path = path_support.merge_path([a_file_model.get_folder_context().get_local_base_path(), a_file_model.get_middle_path()])
    #     encrypter_support.file_encrypt(local_file_path, mock_local_encrypted_path)
    #     path_support.remove_path(local_file_path)
    #     file_db.unsafe_add_update_file_by_model(a_file_model)
    # else:
    # # file_db.add_update_file_by_model(a_file_model)
    #     file_db.add_update_file_by_model(a_file_model)
    # file_db.update_file_model_local_mtime_by_code(a_file_model.get_code(), local_mtime)

def cloud_create_store_file(unencrypt_middle_path:str, file_content:str, cloud_file_db:cloud_repository.CloudRepository, encrypt:bool, mtime:str):
    folder_context:context_model.FolderContext = cloud_file_db.get_folder_context()
    middle_path = ""
    code = encrypter_support.string_hash(unencrypt_middle_path)
    file_name = unencrypt_middle_path.split('/')[-1]
    if encrypt:
        middle_path = '/'.join([encrypter_support.string_source_to_base64_string(p) for p in unencrypt_middle_path.split('/')])
        file_name = encrypter_support.string_source_to_base64_string(file_name)
    else:
        middle_path = unencrypt_middle_path
    # swap_file_path = path_support.merge_path([folder_context.get_swap_base_path(), middle_path])
    # path_support.create_file(swap_file_path, file_content)
    a_cloud_file_model: cloud_file_model.CloudFileModel = cloud_file_model.CloudFileModel(folder_context, code, None, file_name, middle_path, encrypt, mtime)
    cloud_file_db.add_file_model_from_cloud_file_model(a_cloud_file_model)
    # cloud_file_service.upload_file(a_cloud_file_model)

    temp_local_path = path_support.merge_path([test_constant.MOCK_CLOUD_PATH_ROOT, middle_path])
    path_support.create_file(temp_local_path, file_content)
    temp_cloud__path = a_cloud_file_model.get_cloud_file_path()
    
    cloud_file_service.upload_file_by_path(temp_local_path, temp_cloud__path)


# def get_mock_cloud_file_local_path(a_file_model:file_model.FileModel):
#     if a_file_model.get_encrypt():
#         return path_support.merge_path([a_file_model.get_folder_context().get_local_base_path(), a_file_model.get_middle_path()])
#     return a_file_model.get_file_local_path()

# 
# def upload_mock_cloud_to_cloud(local_root_path:str, cloud_root_path):
#     # /Users/i353667/Documents/bin/app/daemon/function/sync-assistant/support/
#     # /Users/i353667/Documents/bin/app/daemon/function/sync-assistant/support/bdwp_support.py
#     # /app/support/
#     file_list = path_support.list_file_recursion(local_root_path)
#     for local_path in file_list:
#         middle_path = local_path.removeprefix(local_root_path)
#         cloud_path = path_support.merge_path([cloud_root_path, middle_path])
#         cloud_file_service.upload_file_by_path(local_path, cloud_path)

# def upload_mock_cloud_to_cloud(mock_cloud_db:repository.FileDB, target_cloud_db_path:str):
#     file_model_dict:dict = mock_cloud_db.get_file_dict()
#     for file_code in file_model_dict.keys():
#         a_file_model:file_model.FileModel = file_model_dict[file_code]
#         # cloud_file_service.upload_file_by_path(get_mock_cloud_file_local_path(a_file_model), a_file_model.get_file_cloud_path())
#         cloud_file_service.upload_file_by_path(a_file_model.get_file_local_path(), a_file_model.get_file_cloud_path())
#     cloud_file_service.upload_file_by_path(mock_cloud_db.get_db_context().get_local_db_path(), target_cloud_db_path)

def clean_test_environment():
    path_support.remove_path(test_constant.BASE_PATH_LOCAL_ROOT)
    cloud_file_service.delete_file_or_folder(test_constant.CLOUD_PATH_ROOT)

def build_index(middle_path:str, mtime:str, encrypt:bool):
    file_code = encrypter_support.string_hash(middle_path)
    file_name = middle_path.split("/")[-1]
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

# def build_from_file_with_mtime(folder_context:file_model.FolderContext, local_file_path:str, mode:str, fs_id:str='',encrypt:bool=False, local_mtime:str="", already_encrypt:bool=False):
#     the_file_model = file_model.build_from_file(folder_context, local_file_path, mode, fs_id,encrypt)
#     the_file_model.set_local_mtime(local_mtime)
#     return the_file_model