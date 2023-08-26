
from service import cloud_file_service
from repository import cloud_repository
from repository import local_repository
from model import local_file_model
from model import cloud_file_model
from model import model_mapper
from support import path_support

from support.log_support import logger

def handle_cloud_update(need_update_files:dict, swap_db:cloud_repository.CloudRepository):
    for key in need_update_files.keys():
        a_local_file_model: local_file_model.LocalFileModel = need_update_files[key]
        logger.info("cloud updating: " + a_local_file_model.get_middle_path())
        new_cloud_file_model: cloud_file_model.CloudFileModel = model_mapper.map_to_cloud_file_model(a_local_file_model)
        try:
            cloud_file_service.upload_file(new_cloud_file_model)
            logger.info("cloud update success: " + a_local_file_model.get_middle_path())
            swap_db.update_mtime_by_key(key, a_local_file_model.get_mtime())
            swap_db.persistence()
        except Exception as err:
            logger.error("cloud update failed: {}".format(a_local_file_model.get_middle_path()))
            logger.error(err)
        

def handle_cloud_create(need_create_files:dict, local_db:local_repository.LocalRepository, swap_db:cloud_repository.CloudRepository):
    for key in need_create_files.keys():
        a_local_file_model: local_file_model.LocalFileModel = need_create_files[key]
        logger.info("cloud creating: " + a_local_file_model.get_middle_path())
        new_cloud_file_model: cloud_file_model.CloudFileModel = model_mapper.map_to_cloud_file_model(a_local_file_model)
        try:
            fs_id = cloud_file_service.upload_file(new_cloud_file_model)
            a_local_file_model.set_fs_id(fs_id)
            logger.info("cloud create success: " + a_local_file_model.get_middle_path())
            swap_db.add_file_model_from_local_file_model(a_local_file_model)
            swap_db.persistence()
            local_db.persistence()
        except Exception as err:
            logger.error("cloud create failed: {}".format(a_local_file_model.get_middle_path()))
            logger.error(err)

def handle_cloud_delete(need_delete_files:dict, swap_db:cloud_repository.CloudRepository):
    for key in need_delete_files.keys():
        a_cloud_file_model:cloud_file_model.CloudFileModel = need_delete_files[key]
        logger.info("cloud deleting: " + a_cloud_file_model.get_middle_path())
        try:
            cloud_file_service.delete_file_or_folder(a_cloud_file_model.get_cloud_file_path())
            logger.info("cloud delete success: " + a_cloud_file_model.get_middle_path())
            swap_db.remove_file_model(key)
            swap_db.persistence()
        except Exception as err:
            logger.error("cloud delete failed: {}".format(a_cloud_file_model.get_middle_path()))
            logger.error(err)


def handle_local_create(should_create_in_local:dict, local_db:local_repository.LocalRepository):
    for key in should_create_in_local.keys():
        a_cloud_file_model:cloud_file_model.CloudFileModel = should_create_in_local[key]
        logger.info("local creating: " + a_cloud_file_model.get_middle_path())
        try:
            cloud_file_service.download_file(a_cloud_file_model)
            logger.info("local create success: " + a_cloud_file_model.get_middle_path())
            local_db.add_file_model_from_cloud_file_model(a_cloud_file_model)
            local_db.persistence()
        except Exception as err:
            logger.error("local create failed: {}".format(a_cloud_file_model.get_middle_path()))
            logger.error(err)


def handle_local_update(should_update_in_local:dict, local_db:local_repository.LocalRepository):
    for key in should_update_in_local.keys():
        a_cloud_file_model:cloud_file_model.CloudFileModel = should_update_in_local[key]
        logger.info("local updating: " + a_cloud_file_model.get_middle_path())
        try:
            cloud_file_service.download_file(a_cloud_file_model)
            logger.info("local update success: " + a_cloud_file_model.get_middle_path())
            local_db.update_mtime_by_key(key, a_cloud_file_model.get_mtime())
            local_db.persistence()
        except Exception as err:
            logger.error("local update failed: {}".format(a_cloud_file_model.get_middle_path()))
            logger.error(err)

def handle_local_delete(should_delete_in_local:dict, local_db:local_repository.LocalRepository):
    for key in should_delete_in_local.keys():
        a_local_file_model: local_file_model.LocalFileModel = should_delete_in_local[key]
        logger.info("local deleting: " + a_local_file_model.get_middle_path())
        try:
            path_support.remove_path(a_local_file_model.get_local_path())
            logger.info("local delete success: " + a_local_file_model.get_middle_path())
            local_db.remove_file_model(key)
            local_db.persistence()
        except Exception as err:
            logger.error("local delete failed: {}".format(a_local_file_model.get_middle_path()))
            logger.error(err)
