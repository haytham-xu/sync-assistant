
from facade import sync_facade
from support.path_support import merge_path, create_folder
from support import file_support
from uttest.test_support import create_store_file, clean_test_environment
from uttest.test_constant import TEST_LOCAL_BASE_PATH, TEST_CLOUD_BASE_PATH, TEST_MODE_MASTER, SAME_FOLDER_NAME, \
    SAME_FILE_NAME, OLD_TIEMSTAMPLE, TEST_FOLDER_CONTEXT, FILE_DEFAULT_CONTENT, TEST_LOCAL_DB, TO_CREATE_FILE_NAME, \
    NEW_TIMESTAMPLE, TO_UPDATE_FILE_NAME, FILE_UPDATE_CONTENT, TEST_LOCAL_DB_PATH, TEST_SWAP_BASE_PATH

def test_sync_push_unencrypt():
    init_test_environment()
    clean_test_environment()

def init_test_environment():
    same_folder_path = merge_path([TEST_LOCAL_BASE_PATH, SAME_FOLDER_NAME])
    create_folder(TEST_LOCAL_BASE_PATH)
    create_folder(same_folder_path)

    same_file_path = merge_path([TEST_LOCAL_BASE_PATH, SAME_FILE_NAME])
    create_store_file(same_file_path, FILE_DEFAULT_CONTENT, TEST_LOCAL_DB, False, OLD_TIEMSTAMPLE, TEST_FOLDER_CONTEXT)
    to_create_file_path = merge_path([TEST_LOCAL_BASE_PATH, TO_CREATE_FILE_NAME])
    create_store_file(to_create_file_path, FILE_DEFAULT_CONTENT, TEST_LOCAL_DB, False, NEW_TIMESTAMPLE, TEST_FOLDER_CONTEXT)
    to_update_file_path = merge_path([TEST_LOCAL_BASE_PATH, TO_UPDATE_FILE_NAME])
    create_store_file(to_update_file_path, FILE_UPDATE_CONTENT, TEST_LOCAL_DB, False, NEW_TIMESTAMPLE, TEST_FOLDER_CONTEXT)
    same_file_2_path = merge_path([TEST_LOCAL_BASE_PATH, SAME_FOLDER_NAME, SAME_FILE_NAME])
    create_store_file(same_file_2_path, FILE_DEFAULT_CONTENT, TEST_LOCAL_DB, False, OLD_TIEMSTAMPLE, TEST_FOLDER_CONTEXT)
    file_support.write_file(TEST_LOCAL_DB_PATH, TEST_LOCAL_DB.to_formatted_json_string()) 
    sync_facade.sync(TEST_LOCAL_BASE_PATH, TEST_CLOUD_BASE_PATH, TEST_SWAP_BASE_PATH, False, TEST_MODE_MASTER)
