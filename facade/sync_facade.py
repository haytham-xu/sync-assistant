

from facade import handler_facade
from service import buffer_service, index_service, cloud_file_service
from repository import repository
from model import context_model
from support import log_support

def sync(local_base_path:str, cloud_base_path:str, swap_base_path:str, encrypt:bool, mode:str, latest_index:dict={}):
    folder_context = context_model.FolderContext(local_base_path, cloud_base_path, swap_base_path)
    db_context = context_model.DBContext(local_base_path, cloud_base_path, swap_base_path)
    buffer_service.create_buffer_folder(folder_context)
    log_support.log_info("sync mode: " + mode)
    if mode == "master":
        sync_push(folder_context, db_context, encrypt, latest_index)
    else:
        sync_pull(folder_context, db_context, encrypt, latest_index)
    buffer_service.remove_buffer_folder(folder_context)

def sync_pull(folder_context:context_model.FolderContext, db_context:context_model.DBContext, encrypt:bool, latest_index:dict):
    log_support.log_info("before download cloud db success.")
    buffer_service.download_cloud_db(folder_context, db_context)
    log_support.log_info("download cloud db success.")
    if latest_index == {}:
        latest_index:dict = index_service.get_latest_index(folder_context.get_local_base_path(), encrypt)
    local_db = repository.FileDB(folder_context, db_context, db_context.get_local_db_path())
    local_db.load_from_db_file(db_context.get_local_db_path())
    swap_db = repository.FileDB(folder_context, db_context, db_context.get_swap_db_path())
    swap_db.load_from_db_file(db_context.get_swap_db_path())
    local_db.update_from_latest_index(latest_index)

    need_create_files:dict = swap_db.get_file_dict_difference(local_db.get_file_dict())
    need_delete_files:dict = local_db.get_file_dict_difference(swap_db.get_file_dict())
    need_update_files:dict = local_db.get_file_dict_intersation_and_mtime_difference(swap_db.get_file_dict())

    handler_facade.handle_local_create(need_create_files, local_db, swap_db, encrypt)
    handler_facade.handle_local_update(need_update_files, local_db, swap_db, encrypt)
    handler_facade.handle_local_delete(need_delete_files, local_db, swap_db)

    local_db.set_file_dict(swap_db.get_file_dict)
    local_db.persistence()

def sync_push(folder_context:context_model.FolderContext, db_context:context_model.DBContext, encrypt:bool, latest_index:dict):
    buffer_service.download_cloud_db(folder_context, db_context)
    if latest_index == {}:
        latest_index:dict = index_service.get_latest_index(folder_context.get_local_base_path(), encrypt)
    local_db = repository.FileDB(folder_context, db_context, db_context.get_local_db_path())
    local_db.load_from_db_file(db_context.get_local_db_path())
    swap_db = repository.FileDB(folder_context, db_context, db_context.get_swap_db_path())
    swap_db.load_from_db_file(db_context.get_swap_db_path())

    local_db.update_from_latest_index(latest_index)
    need_create_files:dict = local_db.get_file_dict_difference(swap_db.get_file_dict())
    need_delete_files:dict = swap_db.get_file_dict_difference(local_db.get_file_dict())
    need_update_files:dict = local_db.get_file_dict_intersation_and_mtime_difference(swap_db.get_file_dict())

    handler_facade.handle_cloud_create(need_create_files, local_db, swap_db)
    handler_facade.handle_cloud_update(need_update_files, local_db, swap_db)
    handler_facade.handle_cloud_delete(need_delete_files, local_db, swap_db)

    local_db.persistence()
    buffer_service.upload_cloud_db(db_context)
