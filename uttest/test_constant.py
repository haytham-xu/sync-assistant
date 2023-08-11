
from support.path_support import merge_path
from model import context_model
from repository import repository
from support.config_support import config

# base
BASE_PATH_LOCAL_ROOT = "./uttest/tmp/"
BASE_PATH_CLOUD_ROOT = config.get_cloud_root_path()
BASE_NAME_TEST_FOLDER = "test_folder"
BASE_NAME_DB = "." + BASE_NAME_TEST_FOLDER + ".json"

# swap
SWAP_NAME_FOLDER = "swap"
SWAP_PATH_ROOT = merge_path([BASE_PATH_LOCAL_ROOT, SWAP_NAME_FOLDER])         # ./uttest/tmp/swap/

# cloud
CLOUD_PATH_ROOT = merge_path([BASE_PATH_CLOUD_ROOT, BASE_NAME_TEST_FOLDER])             # /apps/sync-assistant/test_folder
CLOUD_PATH_DB = merge_path([CLOUD_PATH_ROOT, BASE_NAME_DB])

# local folder
LOCAL_PATH_ROOT = merge_path([BASE_PATH_LOCAL_ROOT, BASE_NAME_TEST_FOLDER])             # ./uttest/tmp/test_folder
LOCAL_PATH_DB = merge_path([LOCAL_PATH_ROOT, BASE_NAME_DB])
LOCAL_FOLDER_CONTEXT = context_model.FolderContext(LOCAL_PATH_ROOT, CLOUD_PATH_ROOT, SWAP_PATH_ROOT)
LOCAL_DB_CONTEXT = context_model.DBContext(LOCAL_PATH_ROOT, CLOUD_PATH_ROOT, SWAP_PATH_ROOT)
LOCAL_DB = repository.FileDB(LOCAL_FOLDER_CONTEXT, LOCAL_DB_CONTEXT, LOCAL_DB_CONTEXT.get_local_db_path())

# mock cloud
MOCK_CLOUD_NAME_FOLDER = "mock_cloud"
MOCK_CLOUD_NAME_DB = "." + MOCK_CLOUD_NAME_FOLDER + ".json"
MOCK_CLOUD_PATH_ROOT = merge_path([BASE_PATH_LOCAL_ROOT, MOCK_CLOUD_NAME_FOLDER])  # ./uttest/tmp/mock_cloud/
MOCK_CLOUD_PATH_DB = merge_path([MOCK_CLOUD_PATH_ROOT, MOCK_CLOUD_NAME_DB])
MOCK_CLOUD_FOLDER_CONTEXT = context_model.FolderContext(MOCK_CLOUD_PATH_ROOT, CLOUD_PATH_ROOT, SWAP_PATH_ROOT)
MOCK_CLOUD_DB_CONTEXT = context_model.DBContext(MOCK_CLOUD_PATH_ROOT, CLOUD_PATH_ROOT, SWAP_PATH_ROOT)
MOCK_CLOUD_DB = repository.FileDB(MOCK_CLOUD_FOLDER_CONTEXT, MOCK_CLOUD_DB_CONTEXT, MOCK_CLOUD_DB_CONTEXT.get_local_db_path())

# test file config
TD_MIDDLE_SAME = "same.md"
TD_MIDDLE_DELETE = "to_delete.md"
TD_MIDDLE_CREATE = "to_create.md"
TD_MIDDLE_UPDATE = "to_update.md"
TD_MIDDLE_SAME_2 = "same_folder/same.md" 

# test data
TD_CONTENT_DEFAULT = "abc"
TD_CONTENT_UPDATE = "abcdef"
TD_OLDTIEM = 1600000000
TD_NEWTIME = 1700000000

# sync mode
TD_MODE_MASTER = "master"
TD_MODE_SUBORDINATE = "subordinate"
