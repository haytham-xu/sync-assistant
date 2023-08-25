

from facade import handler_facade
from service import buffer_service, index_service
from repository import local_repository, cloud_repository, repository_utils
from model import context_model, cloud_file_model, local_file_model
from support import log_support

def sync(local_base_path:str, cloud_base_path:str, swap_base_path:str, encrypt:bool, mode:str, latest_index:dict={}):
    folder_context = context_model.FolderContext(local_base_path, cloud_base_path, swap_base_path)
    buffer_service.create_buffer_folder(folder_context)
    log_support.log_info("sync mode: " + mode)
    if mode == "master":
        sync_push(folder_context, encrypt, latest_index)
    else:
        pass
        # sync_pull(folder_context, encrypt, latest_index)
    input()
    buffer_service.remove_buffer_folder(folder_context)

# def sync_pull(folder_context:context_model.FolderContext, encrypt:bool, latest_index:dict):
#     log_support.log_info("before download cloud db success.")
#     buffer_service.download_cloud_db(folder_context)
#     log_support.log_info("download cloud db success.")
#     if latest_index == {}:
#         latest_index:dict = index_service.get_latest_index(folder_context.get_local_base_path(), encrypt)
#     # local_db = repository.FileDB(folder_context, db_context, db_context.get_local_db_path(), repository.MODE_LOCAL)
#     local_db = local_repository.LocalRepository(folder_context, context_model.get_local_db_name(folder_context), context_model.get_local_db_path(folder_context), {})
#     # local_db.load_from_db_file(db_context.get_local_db_path(), file_model.MODE_LOCAL)
#     local_db.load_from_db_file(context_model.get_local_db_name(folder_context), local_file_model.LocalFileModel)
#     # swap_db = repository.FileDB(folder_context, db_context, db_context.get_swap_db_path(), repository.MODE_CLOUD)
#     swap_db = cloud_repository.CloudRepository(folder_context, context_model.get_cloud_db_name(folder_context), context_model.get_cloud_db_path(folder_context), {}, encrypt)
#     # swap_db.load_from_db_file(db_context.get_swap_db_path(), file_model.MODE_CLOUD)
#     swap_db.load_from_clooud_db_file(context_model.get_cloud_db_path(folder_context), cloud_file_model.CloudFileModel)
#     local_db.update_from_latest_index(latest_index)

#     should_create_in_cloud:dict = local_db.get_file_dict_difference(swap_db)
#     should_update_in_cloud:dict = swap_db.get_file_dict_difference(local_db)
#     should_delete_in_cloud:dict = swap_db.get_file_dict_difference(local_db)

#     # need_create_files:dict = swap_db.get_file_dict_difference(local_db.get_file_dict())
#     need_delete_files:dict = local_db.get_file_dict_difference(swap_db.get_file_dict())
#     need_update_files:dict = local_db.get_file_dict_intersation_and_mtime_difference(swap_db.get_file_dict())

#     handler_facade.handle_local_create(need_create_files, local_db, swap_db, encrypt)
#     handler_facade.handle_local_update(need_update_files, local_db, swap_db, encrypt)
#     handler_facade.handle_local_delete(need_delete_files, local_db, swap_db)

#     local_db.set_file_dict(swap_db.get_file_dict)
#     local_db.persistence()

def sync_push(folder_context:context_model.FolderContext, encrypt:bool, latest_index:dict):

    buffer_service.download_cloud_db(folder_context)
    # input()
    if latest_index == {}:
        latest_index:dict = index_service.get_latest_index(folder_context.get_local_base_path(), encrypt)
    # local_db = repository.FileDB(folder_context, db_context, db_context.get_local_db_path(), repository.MODE_LOCAL)
    local_db = local_repository.LocalRepository(folder_context, context_model.get_local_db_name(folder_context), {})
    # local_db.load_from_db_file(db_context.get_local_db_path(), file_model.MODE_LOCAL)
    local_db.load_from_local_db_file(context_model.get_local_db_name(folder_context))
    # swap_db = repository.FileDB(folder_context, db_context, db_context.get_swap_db_path(), repository.MODE_CLOUD)
    swap_db = cloud_repository.CloudRepository(folder_context, context_model.get_cloud_db_name(folder_context), {}, encrypt)
    # swap_db.load_from_db_file(db_context.get_swap_db_path(), file_model.MODE_CLOUD)
    swap_db.load_from_cloud_db_file(context_model.get_swap_db_path(folder_context))
    local_db.update_from_latest_index(latest_index)

    should_create_in_cloud:dict = repository_utils.get_file_dict_difference_from_cloud_repository(local_db, swap_db)#   local_db.get_file_dict_difference(swap_db)
    should_update_in_cloud:dict = repository_utils.get_file_dict_intersation_and_mtime_difference_from_cloud_repository(local_db, swap_db)# local_db.get_file_dict_difference(swap_db)
    should_delete_in_cloud:dict = repository_utils.get_file_dict_difference_from_local_repository(swap_db, local_db) #swap_db.get_file_dict_difference(local_db)

    # need_create_files:dict = local_db.get_file_dict_difference(swap_db.get_file_dict())
    # need_delete_files:dict = swap_db.get_file_dict_difference(local_db.get_file_dict())
    # need_update_files:dict = local_db.get_file_dict_intersation_and_mtime_difference(swap_db.get_file_dict())

    handler_facade.handle_cloud_create(should_create_in_cloud, local_db, swap_db)
    handler_facade.handle_cloud_update(should_update_in_cloud, swap_db)
    handler_facade.handle_cloud_delete(should_delete_in_cloud, swap_db)

    buffer_service.upload_cloud_db(folder_context)
