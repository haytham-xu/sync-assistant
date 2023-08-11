import json

from facade import sync_facade
from service import cloud_file_service
from model import file_model
from support import file_support, path_support, encrypter_support
from uttest import test_support, test_constant

def test_sync_push_unencrypt():
    try:
        init_test_environment()
        trigger()
        check()
    except Exception as err:
        print(err.with_traceback())
    finally:
        test_support.clean_test_environment()

def init_test_environment():
    # init swap folder
    path_support.create_folder(test_constant.SWAP_PATH_ROOT)
    # init local folder
    path_support.create_folder(test_constant.LOCAL_PATH_ROOT)
    test_support.local_create_store_file(test_constant.TD_MIDDLE_SAME, test_constant.TD_CONTENT_DEFAULT, test_constant.LOCAL_DB, False, test_constant.TD_OLDTIEM)
    test_support.local_create_store_file(test_constant.TD_MIDDLE_CREATE, test_constant.TD_CONTENT_DEFAULT, test_constant.LOCAL_DB, False, test_constant.TD_NEWTIME)
    test_support.local_create_store_file(test_constant.TD_MIDDLE_UPDATE, test_constant.TD_CONTENT_UPDATE, test_constant.LOCAL_DB, False, test_constant.TD_NEWTIME)
    test_support.local_create_store_file(test_constant.TD_MIDDLE_SAME_2, test_constant.TD_CONTENT_DEFAULT, test_constant.LOCAL_DB, False, test_constant.TD_OLDTIEM)
    file_support.write_file(test_constant.LOCAL_PATH_DB, test_constant.LOCAL_DB.to_formatted_json_string())
    # init mock cloud and cloud folder
    path_support.create_folder(test_constant.MOCK_CLOUD_PATH_ROOT)
    test_support.local_create_store_file(test_constant.TD_MIDDLE_SAME, test_constant.TD_CONTENT_DEFAULT, test_constant.MOCK_CLOUD_DB, False, test_constant.TD_OLDTIEM)
    test_support.local_create_store_file(test_constant.TD_MIDDLE_UPDATE, test_constant.TD_CONTENT_DEFAULT, test_constant.MOCK_CLOUD_DB, False, test_constant.TD_OLDTIEM)
    test_support.local_create_store_file(test_constant.TD_MIDDLE_SAME_2, test_constant.TD_CONTENT_DEFAULT, test_constant.MOCK_CLOUD_DB, False, test_constant.TD_OLDTIEM)
    test_support.local_create_store_file(test_constant.TD_MIDDLE_DELETE, test_constant.TD_CONTENT_DEFAULT, test_constant.MOCK_CLOUD_DB, False, test_constant.TD_OLDTIEM)
    file_support.write_file(test_constant.MOCK_CLOUD_PATH_DB, test_constant.MOCK_CLOUD_DB.to_formatted_json_string())
    test_support.upload_mock_cloud_to_cloud(test_constant.MOCK_CLOUD_DB, test_constant.LOCAL_DB.get_db_context().get_cloud_db_path())

def trigger():
        # init latest indexs
    latest_index = test_support.build_indexs([
        test_support.build_index(test_constant.TD_MIDDLE_SAME, test_constant.TD_OLDTIEM, False),
        test_support.build_index(test_constant.TD_MIDDLE_CREATE, test_constant.TD_NEWTIME, False),
        test_support.build_index(test_constant.TD_MIDDLE_UPDATE, test_constant.TD_NEWTIME, False),
        test_support.build_index(test_constant.TD_MIDDLE_SAME_2, test_constant.TD_OLDTIEM, False),
    ])
    sync_facade.sync(test_constant.LOCAL_PATH_ROOT, test_constant.CLOUD_PATH_ROOT, test_constant.SWAP_PATH_ROOT, False, test_constant.TD_MODE_MASTER, latest_index)

def check():
    assert cloud_file_service.is_exist(path_support.merge_path([test_constant.CLOUD_PATH_ROOT, test_constant.TD_MIDDLE_CREATE])) == True
    assert cloud_file_service.is_exist(path_support.merge_path([test_constant.CLOUD_PATH_ROOT, test_constant.TD_MIDDLE_SAME])) == True
    assert cloud_file_service.is_exist(path_support.merge_path([test_constant.CLOUD_PATH_ROOT, test_constant.TD_MIDDLE_SAME_2])) == True
    assert cloud_file_service.is_exist(path_support.merge_path([test_constant.CLOUD_PATH_ROOT, test_constant.TD_MIDDLE_UPDATE])) == True
    assert cloud_file_service.is_exist(path_support.merge_path([test_constant.CLOUD_PATH_ROOT, test_constant.TD_MIDDLE_DELETE])) == False

    assert cloud_file_service.get_file_content_by_path(test_constant.CLOUD_PATH_ROOT, test_constant.TD_MIDDLE_UPDATE) == test_constant.TD_CONTENT_UPDATE

    assert path_support.is_exist(path_support.merge_path([test_constant.LOCAL_PATH_ROOT, test_constant.TD_MIDDLE_CREATE])) == True
    assert path_support.is_exist(path_support.merge_path([test_constant.LOCAL_PATH_ROOT, test_constant.TD_MIDDLE_SAME])) == True
    assert path_support.is_exist(path_support.merge_path([test_constant.LOCAL_PATH_ROOT, test_constant.TD_MIDDLE_SAME_2])) == True
    assert path_support.is_exist(path_support.merge_path([test_constant.LOCAL_PATH_ROOT, test_constant.TD_MIDDLE_UPDATE])) == True
    assert path_support.is_exist(path_support.merge_path([test_constant.LOCAL_PATH_ROOT, test_constant.TD_MIDDLE_DELETE])) == False

    assert file_support.read_file_as_string(path_support.merge_path([test_constant.LOCAL_PATH_ROOT, test_constant.TD_MIDDLE_UPDATE])) == test_constant.TD_CONTENT_UPDATE


    code_file_create = encrypter_support.string_hash(test_constant.TD_MIDDLE_CREATE)
    code_file_same = encrypter_support.string_hash(test_constant.TD_MIDDLE_SAME)
    code_file_same_2 = encrypter_support.string_hash(test_constant.TD_MIDDLE_SAME_2)
    code_file_update = encrypter_support.string_hash(test_constant.TD_MIDDLE_UPDATE)

    local_db_dict = json.loads(file_support.read_file_as_string(test_constant.LOCAL_PATH_DB))
    assert len(local_db_dict) == 4
    assert code_file_create in local_db_dict
    assert code_file_same in local_db_dict
    assert code_file_same_2 in local_db_dict
    assert code_file_update in local_db_dict

    assert local_db_dict[code_file_create][file_model.KEY_LOCAL_MTIME] == test_constant.TD_NEWTIME
    assert local_db_dict[code_file_same][file_model.KEY_LOCAL_MTIME] == test_constant.TD_OLDTIEM
    assert local_db_dict[code_file_same_2][file_model.KEY_LOCAL_MTIME] == test_constant.TD_OLDTIEM
    assert local_db_dict[code_file_update][file_model.KEY_LOCAL_MTIME] == test_constant.TD_NEWTIME

    cloud_db_dict = json.loads(cloud_file_service.get_file_content_by_path(test_constant.CLOUD_PATH_ROOT, test_constant.BASE_NAME_DB))
    assert len(cloud_db_dict) == 4
    assert code_file_create in cloud_db_dict
    assert code_file_same in cloud_db_dict
    assert code_file_same_2 in cloud_db_dict
    assert code_file_update in cloud_db_dict

    assert cloud_db_dict[code_file_create][file_model.KEY_LOCAL_MTIME] == test_constant.TD_NEWTIME
    assert cloud_db_dict[code_file_same][file_model.KEY_LOCAL_MTIME] == test_constant.TD_OLDTIEM
    assert cloud_db_dict[code_file_same_2][file_model.KEY_LOCAL_MTIME] == test_constant.TD_OLDTIEM
    assert cloud_db_dict[code_file_update][file_model.KEY_LOCAL_MTIME] == test_constant.TD_NEWTIME
