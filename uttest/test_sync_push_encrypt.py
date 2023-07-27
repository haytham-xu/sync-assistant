
from uttest import test_constant
from support.config_support import config

def test_sync_push_encrypt():
    sync_folder_list = [{
        config.get_key_cloud_folder(): test_constant.TEST_CLOUD_BASE_PATH,
        config.get_key_local_folder(): test_constant.TEST_LOCAL_BASE_PATH,
        config.get_key_encrypt(): True,
        config.get_key_mode(): test_constant.TEST_MODE_MASTER
    }]
    config.set_sync_folder(sync_folder_list)