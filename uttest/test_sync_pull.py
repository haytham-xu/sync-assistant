

from support.path_support import merge_path, create_folder, remove_path
from uttest.test_support import create_store_file
from uttest import test_constant

def test_sync_pull():
    init_test_environment()
    input()
    clean_test_environment()

def init_test_environment():
    same_folder_path = merge_path([test_constant.TEST_LOCAL_BASE_PATH, test_constant.SAME_FOLDER_NAME])
    create_folder(test_constant.TEST_LOCAL_BASE_PATH)
    create_folder(same_folder_path)

    same_file_path = merge_path([test_constant.TEST_LOCAL_BASE_PATH, test_constant.SAME_FILE_NAME])
    create_store_file(same_file_path, test_constant.FILE_DEFAULT_CONTENT, test_constant.TEST_LOCAL_DB, False, test_constant.OLD_TIEMSTAMPLE, test_constant.TEST_FOLDER_CONTEXT)
    to_create_file_path = merge_path([test_constant.TEST_LOCAL_BASE_PATH, test_constant.TO_CREATE_FILE_NAME])
    create_store_file(to_create_file_path, test_constant.FILE_DEFAULT_CONTENT, test_constant.TEST_LOCAL_DB, False, test_constant.NEW_TIMESTAMPLE, test_constant.TEST_FOLDER_CONTEXT)
    to_update_file_path = merge_path([test_constant.TEST_LOCAL_BASE_PATH, test_constant.TO_UPDATE_FILE_NAME])
    create_store_file(to_update_file_path, test_constant.FILE_UPDATE_CONTENT, test_constant.TEST_LOCAL_DB, False, test_constant.NEW_TIMESTAMPLE, test_constant.TEST_FOLDER_CONTEXT)
    same_file_2_path = merge_path([test_constant.TEST_LOCAL_BASE_PATH, test_constant.SAME_FOLDER_NAME, test_constant.SAME_FILE_NAME])
    create_store_file(same_file_2_path, test_constant.FILE_DEFAULT_CONTENT, test_constant.TEST_LOCAL_DB, False, test_constant.OLD_TIEMSTAMPLE, test_constant.TEST_FOLDER_CONTEXT)
    # todo

def clean_test_environment():
    remove_path(test_constant.TEST_LOCAL_BASE_PATH)
