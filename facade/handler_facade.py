
from service import cloud_file_service
from repository import cloud_repository, local_repository
from model import local_file_model, cloud_file_model, model_mapper
from support import path_support, log_support

def handle_cloud_update(need_create_files:dict, swap_db:cloud_repository.CloudRepository):
    for key in need_create_files.keys():
        a_local_file_model: local_file_model.LocalFileModel = need_create_files[key]
        log_support.log_info("cloud updating: " + a_local_file_model.get_middle_path())
        new_cloud_file_model: cloud_file_model.CloudFileModel = model_mapper.map_to_cloud_file_model(a_local_file_model)
        cloud_file_service.upload_file(new_cloud_file_model)
        log_support.log_info("cloud update success: " + a_local_file_model.get_middle_path())
        swap_db.update_mtime_by_key(key, a_local_file_model.get_mtime())
        swap_db.persistence()

def handle_cloud_create(need_create_files:dict, local_db:local_repository.LocalRepository, swap_db:cloud_repository.CloudRepository):
    for key in need_create_files.keys():
        a_local_file_model: local_file_model.LocalFileModel = need_create_files[key]
        log_support.log_info("cloud creating: " + a_local_file_model.get_middle_path())
        new_cloud_file_model: cloud_file_model.CloudFileModel = model_mapper.map_to_cloud_file_model(a_local_file_model)
        fs_id = cloud_file_service.upload_file(new_cloud_file_model)
        a_local_file_model.set_fs_id(fs_id)
        log_support.log_info("cloud create success: " + a_local_file_model.get_middle_path())
        swap_db.add_file_model_from_local_file_model(a_local_file_model)
        swap_db.persistence()
        local_db.persistence()

def handle_cloud_delete(need_create_files:dict, swap_db:cloud_repository.CloudRepository):
    for key in need_create_files.keys():
        a_cloud_file_model:cloud_file_model.CloudFileModel = need_create_files[key]
        log_support.log_info("cloud deleting: " + a_cloud_file_model.get_middle_path())
        # log_support.log_delete_local_file_success(a_local_file_model)
        # the_cloud_file_model:cloud_file_model.CloudFileModel = model_mapper.map_to_cloud_file_model(a_cloud_file_model)
        cloud_file_service.delete_file_or_folder(a_cloud_file_model.get_cloud_file_path())
        log_support.log_info("cloud delete success: " + a_cloud_file_model.get_middle_path())
        # local_db.remove_file_model(key)
        swap_db.remove_file_model(key)
        swap_db.persistence()
        # local_db.persistence()

# def handle_local_create(need_create_files:dict, local_db:repository.FileDB, swap_db:repository.FileDB, encrypt:bool):
#     pass
#     # handle_local_update(need_create_files, local_db, swap_db)

# def handle_local_update(need_create_files:dict, local_db:repository.FileDB, swap_db:repository.FileDB):
#     pass
    # for key in need_create_files.keys():
    #     a_file_model:file_model.FileModel = need_create_files[key]
    #     log_support.log_info("local creating/updating: " + a_file_model.get_file_local_path())
    #     cloud_file_service.download_file_by_fsid(a_file_model)
    #     swap_db.add_update_file_by_model(a_file_model)
    #     local_db.add_update_file_by_model(a_file_model)
    #     swap_db.persistence()
    #     local_db.persistence()

# def handle_local_delete(need_create_files:dict, local_db:repository.FileDB, swap_db:repository.FileDB):
#     pass
    # for key in need_create_files.keys():
    #     a_file_model:file_model.FileModel = need_create_files[key]
    #     log_support.log_info("local deleting: " + a_file_model.get_file_local_path())
    #     path_support.remove_path(a_file_model.get_file_local_path())
    #     local_db.remove_file_model(key)
    #     swap_db.remove_file_model(key)
    #     swap_db.persistence()
    #     local_db.persistence()
