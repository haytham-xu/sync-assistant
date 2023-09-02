

from uttest.sync_uttest import test_constant
from uttest.sync_uttest import test_sync_push_unencrypt
from uttest.sync_uttest import test_sync_push_encrypt
from uttest.sync_uttest import test_sync_pull_unencrypt
from uttest.sync_uttest import test_sync_pull_encrypt

from support.config_support import config

def run_test():
    config.set_swap_folder_path(test_constant.SWAP_PATH_ROOT)
    config.set_local_root_path(test_constant.BASE_PATH_LOCAL_ROOT)
    test_sync_push_unencrypt.test_sync_push_unencrypt()
    test_sync_push_encrypt.test_sync_push_encrypt()
    test_sync_pull_unencrypt.test_sync_pull_unencrypt()
    test_sync_pull_encrypt.test_sync_pull_encrypt()