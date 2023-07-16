
from service import cloud_file_service
from repository import repository
from model import file_model
from support import path_support, log_support

def handle_cloud_update(need_create_files:dict, local_db:repository.FileDB, swap_db:repository.FileDB):
    for key in need_create_files.keys():
        a_file_model:file_model.FileModel = need_create_files[key]
        fs_id = cloud_file_service.upload_file(a_file_model)
        a_file_model.set_fs_id(fs_id)
        log_support.log_upload_file_success(a_file_model)
        # todo: will this set value successfully?

def handle_cloud_create(need_create_files:dict, local_db:repository.FileDB, swap_db:repository.FileDB):
    handle_cloud_update(need_create_files, local_db, swap_db)

def handle_cloud_delete(need_create_files:dict, local_db:repository.FileDB, swap_db:repository.FileDB):
    for key in need_create_files.keys():
        a_file_model:file_model.FileModel = need_create_files[key]
        log_support.log_delete_local_file_success(a_file_model)
        cloud_file_service.delete_file_or_folder(a_file_model.get_file_cloud_path())
        local_db.remove_file_model(key)

def handle_local_create(need_create_files:dict, local_db:repository.FileDB, swap_db:repository.FileDB, encrypt:bool):
    handle_local_update(need_create_files, local_db, swap_db)
    # update local db

def handle_local_update(need_create_files:dict, local_db:repository.FileDB, swap_db:repository.FileDB):
    for key in need_create_files.keys():
        a_file_model:file_model.FileModel = need_create_files[key]
        cloud_file_service.download_file_by_fsid(a_file_model)
        # update local db

def handle_local_delete(need_create_files:dict, local_db:repository.FileDB, swap_db:repository.FileDB):
    for key in need_create_files.keys():
        a_file_model:file_model.FileModel = need_create_files[key]
        path_support.remove_path(a_file_model.get_file_local_path())
