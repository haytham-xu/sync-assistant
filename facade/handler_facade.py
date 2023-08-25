
from service import cloud_file_service
from repository import cloud_repository
from repository import local_repository
from model import local_file_model
from model import cloud_file_model
from model import model_mapper
from support import log_support

from support.log_support import logger

def handle_cloud_update(need_create_files:dict, swap_db:cloud_repository.CloudRepository):
    for key in need_create_files.keys():
        a_local_file_model: local_file_model.LocalFileModel = need_create_files[key]
        logger.info("cloud updating: " + a_local_file_model.get_middle_path())
        new_cloud_file_model: cloud_file_model.CloudFileModel = model_mapper.map_to_cloud_file_model(a_local_file_model)
        cloud_file_service.upload_file(new_cloud_file_model)
        logger.info("cloud update success: " + a_local_file_model.get_middle_path())
        swap_db.update_mtime_by_key(key, a_local_file_model.get_mtime())
        swap_db.persistence()

def handle_cloud_create(need_create_files:dict, local_db:local_repository.LocalRepository, swap_db:cloud_repository.CloudRepository):
    for key in need_create_files.keys():
        a_local_file_model: local_file_model.LocalFileModel = need_create_files[key]
        logger.info("cloud creating: " + a_local_file_model.get_middle_path())
        new_cloud_file_model: cloud_file_model.CloudFileModel = model_mapper.map_to_cloud_file_model(a_local_file_model)
        fs_id = cloud_file_service.upload_file(new_cloud_file_model)
        a_local_file_model.set_fs_id(fs_id)
        logger.info("cloud create success: " + a_local_file_model.get_middle_path())
        swap_db.add_file_model_from_local_file_model(a_local_file_model)
        swap_db.persistence()
        local_db.persistence()

def handle_cloud_delete(need_create_files:dict, swap_db:cloud_repository.CloudRepository):
    for key in need_create_files.keys():
        a_cloud_file_model:cloud_file_model.CloudFileModel = need_create_files[key]
        logger.info("cloud deleting: " + a_cloud_file_model.get_middle_path())
        cloud_file_service.delete_file_or_folder(a_cloud_file_model.get_cloud_file_path())
        logger.info("cloud delete success: " + a_cloud_file_model.get_middle_path())
        swap_db.remove_file_model(key)
        swap_db.persistence()
