

from model import context_model
from support import encrypter_support
from support import path_support

from support.config_support import config

# base
BASE_PATH_LOCAL_ROOT = "./uttest/tmp/"
BASE_PATH_CLOUD_ROOT = config.get_cloud_root_path()
BASE_NAME_TEST_FOLDER = "test_folder"
BASE_NAME_DB = "." + BASE_NAME_TEST_FOLDER + ".json"
BASE_UPLOAD_CLOUD_DB_GAP = 2


# swap
SWAP_NAME_FOLDER = "swap"
SWAP_PATH_ROOT = path_support.merge_path([BASE_PATH_LOCAL_ROOT, SWAP_NAME_FOLDER])                   # ./uttest/tmp/swap
# cloud
CLOUD_PATH_ROOT = path_support.merge_path([BASE_PATH_CLOUD_ROOT, BASE_NAME_TEST_FOLDER])             # /apps/sync-assistant/test_folder
CLOUD_PATH_DB = path_support.merge_path([CLOUD_PATH_ROOT, BASE_NAME_DB])
# local folder
LOCAL_PATH_ROOT = path_support.merge_path([BASE_PATH_LOCAL_ROOT, BASE_NAME_TEST_FOLDER])             # ./uttest/tmp/test_folder
LOCAL_PATH_DB = path_support.merge_path([LOCAL_PATH_ROOT, BASE_NAME_DB])

# folder context
BASE_FOLDER_CONTEXT = context_model.FolderContext(LOCAL_PATH_ROOT, CLOUD_PATH_ROOT, SWAP_PATH_ROOT)

# mock cloud
MOCK_CLOUD_NAME_FOLDER = "mock_cloud"
MOCK_CLOUD_PATH_ROOT = path_support.merge_path([BASE_PATH_LOCAL_ROOT, MOCK_CLOUD_NAME_FOLDER])  # ./uttest/tmp/mock_cloud/
MOCK_CLOUD_PATH_DB = path_support.merge_path([MOCK_CLOUD_PATH_ROOT, BASE_NAME_DB])

# test file config
TD_MIDDLE_SAME = "same.md"
TD_MIDDLE_DELETE = "to_delete.md"
TD_MIDDLE_CREATE = "to_create.md"
TD_MIDDLE_UPDATE = "to_update.md"
TD_MIDDLE_SAME_2 = "same_folder/same.md"

def get_encrypt_path(source_path:str):
    return '/'.join([encrypter_support.string_source_to_base64_string(p) for p in source_path.split('/')])

TD_MIDDLE_SAME_ENCRYPT = get_encrypt_path(TD_MIDDLE_SAME)
TD_MIDDLE_DELETE_ENCRYPT = get_encrypt_path(TD_MIDDLE_DELETE)
TD_MIDDLE_CREATE_ENCRYPT = get_encrypt_path(TD_MIDDLE_CREATE)
TD_MIDDLE_UPDATE_ENCRYPT = get_encrypt_path(TD_MIDDLE_UPDATE)
TD_MIDDLE_SAME_2_ENCRYPT = get_encrypt_path(TD_MIDDLE_SAME_2)

# test data
TD_CONTENT_DEFAULT = "abc"
TD_CONTENT_UPDATE = "abcdef"
TD_OLDTIEM = 1600000000
TD_NEWTIME = 1700000000

# sync mode
TD_MODE_MASTER = "master"
TD_MODE_SUBORDINATE = "subordinate"
