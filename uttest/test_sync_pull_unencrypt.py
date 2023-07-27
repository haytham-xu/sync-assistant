

from support.path_support import merge_path, create_folder, remove_path
from uttest.test_support import create_store_file
from uttest import test_constant
from support.config_support import config

def test_sync_pull_unencrypt():
    sync_folder_list = [{
        config.get_key_cloud_folder(): test_constant.TEST_CLOUD_BASE_PATH,
        config.get_key_local_folder(): test_constant.TEST_LOCAL_BASE_PATH,
        config.get_key_encrypt(): False,
        config.get_key_mode(): test_constant.TEST_MODE_SUBORDINATE
    }]
    config.set_sync_folder(sync_folder_list)
