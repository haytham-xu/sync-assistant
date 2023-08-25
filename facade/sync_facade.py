
from facade import handler_facade
from service import buffer_service
from service import  index_service
from repository import local_repository
from repository import  cloud_repository
from repository import  repository_utils
from model import context_model
from support.log_support import logger

def sync(local_base_path:str, cloud_base_path:str, swap_base_path:str, encrypt:bool, mode:str, latest_index:dict={}):
    folder_context = context_model.FolderContext(local_base_path, cloud_base_path, swap_base_path)
    buffer_service.create_buffer_folder(folder_context)
    logger.info("<---- mode: {} | local path: {} | encrypt: {} ---->".format(mode, local_base_path, encrypt))
    if mode == "master":
        sync_push(folder_context, encrypt, latest_index)
    else:
        pass
    buffer_service.remove_buffer_folder(folder_context)

def sync_push(folder_context:context_model.FolderContext, encrypt:bool, latest_index:dict):
    buffer_service.download_cloud_db(folder_context)
    if latest_index == {}:
        latest_index:dict = index_service.get_latest_index(folder_context.get_local_base_path(), encrypt)
    local_db = local_repository.LocalRepository(folder_context, context_model.get_local_db_name(folder_context), {})
    local_db.load_from_local_db_file(context_model.get_local_db_name(folder_context))
    swap_db = cloud_repository.CloudRepository(folder_context, context_model.get_cloud_db_name(folder_context), {}, encrypt)
    swap_db.load_from_cloud_db_file(context_model.get_swap_db_path(folder_context))
    local_db.update_from_latest_index(latest_index)

    should_create_in_cloud:dict = repository_utils.get_file_dict_difference_from_cloud_repository(local_db, swap_db)
    should_update_in_cloud:dict = repository_utils.get_file_dict_intersation_and_mtime_difference_from_cloud_repository(local_db, swap_db)
    should_delete_in_cloud:dict = repository_utils.get_file_dict_difference_from_local_repository(swap_db, local_db)

    handler_facade.handle_cloud_create(should_create_in_cloud, local_db, swap_db)
    handler_facade.handle_cloud_update(should_update_in_cloud, swap_db)
    handler_facade.handle_cloud_delete(should_delete_in_cloud, swap_db)

    buffer_service.upload_cloud_db(folder_context)
