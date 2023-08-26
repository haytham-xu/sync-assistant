
from uttest import test_constant
from uttest import test_sync_push_unencrypt
from uttest import test_sync_push_encrypt
from uttest import test_sync_pull_unencrypt
from uttest import test_sync_pull_encrypt

from support.config_support import config

if __name__ == "__main__":
    config.set_swap_folder_path(test_constant.SWAP_PATH_ROOT)
    config.set_local_root_path(test_constant.BASE_PATH_LOCAL_ROOT)
    test_sync_push_unencrypt.test_sync_push_unencrypt()
    test_sync_push_encrypt.test_sync_push_encrypt()
    test_sync_pull_unencrypt.test_sync_pull_unencrypt()
    test_sync_pull_encrypt.test_sync_pull_encrypt()
