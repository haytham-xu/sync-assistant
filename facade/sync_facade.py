

from facade import handler_facade
from service import buffer_service, index_service, cloud_file_service
from repository import repository
from model import context_model

def sync(local_base_path, cloud_base_path, swap_base_path, encrypt, mode):
    folder_context = context_model.FolderContext(local_base_path, cloud_base_path, swap_base_path)
    db_context = context_model.DBContext(local_base_path, cloud_base_path, swap_base_path)
    buffer_service.create_buffer_folder(folder_context)
    if mode == "master":
        sync_push(folder_context, db_context, encrypt)
    else:
        sync_pull(folder_context, db_context, encrypt)
    buffer_service.remove_buffer_folder(folder_context)

def sync_pull(folder_context:context_model.FolderContext, db_context:context_model.DBContext, encrypt:bool):
    cloud_file_service.download_file(folder_context.get_swap_base_path(), folder_context.get_cloud_base_path(), db_context.get_db_name())
    latest_index:dict = index_service.get_latest_index(folder_context.get_local_base_path(), encrypt)
    local_db = repository.FileDB(folder_context, db_context, db_context.get_local_db_path())
    swap_db = repository.FileDB(folder_context, db_context, db_context.get_swap_db_path())
    local_db.update_from_latest_index(latest_index)

    need_create_files:dict = swap_db.get_file_dict_difference(local_db.get_file_dict())
    need_delete_files:dict = local_db.get_file_dict_difference(swap_db.get_file_dict())
    need_update_files:dict = local_db.get_file_dict_intersation_and_mtime_difference(swap_db.get_file_dict())

    handler_facade.handle_local_create(need_create_files, local_db, swap_db, encrypt)
    handler_facade.handle_local_update(need_update_files, local_db, swap_db, encrypt)
    handler_facade.handle_local_delete(need_delete_files, local_db, swap_db)

    local_db.set_file_dict(swap_db.get_file_dict)
    local_db.persistence()

def sync_push(folder_context:context_model.FolderContext, db_context:context_model.DBContext, encrypt:bool):
    cloud_file_service.download_file(folder_context.get_swap_base_path(), folder_context.get_cloud_base_path(), db_context.get_db_name())
    latest_index:dict = index_service.get_latest_index(folder_context.get_local_base_path(), encrypt)
    local_db = repository.FileDB(folder_context, db_context, db_context.get_local_db_path())
    swap_db = repository.FileDB(folder_context, db_context, db_context.get_swap_db_path())

    local_db.update_from_latest_index(latest_index)
    need_create_files:dict = local_db.get_file_dict_difference(swap_db.get_file_dict())
    need_delete_files:dict = swap_db.get_file_dict_difference(local_db.get_file_dict())
    need_update_files:dict = local_db.get_file_dict_intersation_and_mtime_difference(swap_db.get_file_dict())

    handler_facade.handle_cloud_create(need_create_files, local_db, swap_db, encrypt)
    handler_facade.handle_cloud_update(need_update_files, local_db, swap_db, encrypt)
    handler_facade.handle_cloud_delete(need_delete_files, local_db, swap_db)

    local_db.persistence()
    cloud_file_service.upload_file(db_context.get_local_db_path(), db_context.get_cloud_db_path())
