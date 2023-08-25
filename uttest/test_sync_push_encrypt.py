
from facade import sync_facade
from service import cloud_file_service
from model import local_file_model, cloud_file_model, base_file_model
from repository import local_repository, cloud_repository
from support import file_support, path_support, encrypter_support
from uttest import test_support, test_constant

import json

def test_sync_push_encrypt():
    try:
        init_test_environment()
        trigger()
        check()
    except Exception as err:
        print(err.with_traceback())
    finally:
        print("ready to clean")
        input()
        test_support.clean_test_environment()

def init_test_environment():
    # init swap folder
    path_support.create_folder(test_constant.SWAP_PATH_ROOT)
    # init local folder
    path_support.create_folder(test_constant.LOCAL_PATH_ROOT)

    # init db
    local_db = local_repository.LocalRepository(test_constant.BASE_FOLDER_CONTEXT, test_constant.BASE_NAME_DB, {})
    test_support.local_create_store_file(test_constant.TD_MIDDLE_SAME, test_constant.TD_CONTENT_DEFAULT, local_db, True, test_constant.TD_OLDTIEM)
    test_support.local_create_store_file(test_constant.TD_MIDDLE_CREATE, test_constant.TD_CONTENT_DEFAULT, local_db, True, test_constant.TD_NEWTIME)
    test_support.local_create_store_file(test_constant.TD_MIDDLE_UPDATE, test_constant.TD_CONTENT_UPDATE, local_db, True, test_constant.TD_NEWTIME)
    test_support.local_create_store_file(test_constant.TD_MIDDLE_SAME_2, test_constant.TD_CONTENT_DEFAULT, local_db, True, test_constant.TD_OLDTIEM)
    file_support.write_file(test_constant.LOCAL_PATH_DB, local_db.to_formatted_json_string())

    # test_support.local_create_store_file(test_constant.TD_MIDDLE_SAME, test_constant.TD_CONTENT_DEFAULT, test_constant.LOCAL_DB, True, test_constant.TD_OLDTIEM, file_model.MODE_LOCAL)
    # test_support.local_create_store_file(test_constant.TD_MIDDLE_CREATE, test_constant.TD_CONTENT_DEFAULT, test_constant.LOCAL_DB, True, test_constant.TD_NEWTIME, file_model.MODE_LOCAL)
    # test_support.local_create_store_file(test_constant.TD_MIDDLE_UPDATE, test_constant.TD_CONTENT_UPDATE, test_constant.LOCAL_DB, True, test_constant.TD_NEWTIME, file_model.MODE_LOCAL)
    # test_support.local_create_store_file(test_constant.TD_MIDDLE_SAME_2, test_constant.TD_CONTENT_DEFAULT, test_constant.LOCAL_DB, True, test_constant.TD_OLDTIEM, file_model.MODE_LOCAL)
    # file_support.write_file(test_constant.LOCAL_PATH_DB, test_constant.LOCAL_DB.to_formatted_json_string())
    # init mock cloud and cloud folder
    # path_support.create_folder(test_constant.MOCK_CLOUD_PATH_ROOT)
    # test_support.local_create_store_file(test_constant.TD_MIDDLE_SAME, test_constant.TD_CONTENT_DEFAULT, test_constant.MOCK_CLOUD_DB, True, test_constant.TD_OLDTIEM, file_model.MODE_CLOUD)
    # test_support.local_create_store_file(test_constant.TD_MIDDLE_UPDATE, test_constant.TD_CONTENT_DEFAULT, test_constant.MOCK_CLOUD_DB, True, test_constant.TD_OLDTIEM, file_model.MODE_CLOUD)
    # test_support.local_create_store_file(test_constant.TD_MIDDLE_SAME_2, test_constant.TD_CONTENT_DEFAULT, test_constant.MOCK_CLOUD_DB, True, test_constant.TD_OLDTIEM, file_model.MODE_CLOUD)
    # test_support.local_create_store_file(test_constant.TD_MIDDLE_DELETE, test_constant.TD_CONTENT_DEFAULT, test_constant.MOCK_CLOUD_DB, True, test_constant.TD_OLDTIEM, file_model.MODE_CLOUD)
    # file_support.write_file(test_constant.MOCK_CLOUD_PATH_DB, test_constant.MOCK_CLOUD_DB.to_formatted_json_string())
    # # test_support.upload_mock_cloud_to_cloud(test_constant.MOCK_CLOUD_DB, test_constant.LOCAL_DB.get_db_context().get_cloud_db_path())
    # test_support.upload_mock_cloud_to_cloud(test_constant.MOCK_CLOUD_FOLDER_CONTEXT.get_local_base_path(), test_constant.MOCK_CLOUD_FOLDER_CONTEXT.get_cloud_base_path())

        # init mock cloud and cloud folder
    path_support.create_folder(test_constant.MOCK_CLOUD_PATH_ROOT)
    mock_cloud_db = cloud_repository.CloudRepository(test_constant.BASE_FOLDER_CONTEXT, test_constant.BASE_NAME_DB, {}, True)
    test_support.cloud_create_store_file(test_constant.TD_MIDDLE_SAME, test_constant.TD_CONTENT_DEFAULT, mock_cloud_db, True, test_constant.TD_OLDTIEM)
    test_support.cloud_create_store_file(test_constant.TD_MIDDLE_UPDATE, test_constant.TD_CONTENT_DEFAULT, mock_cloud_db, True, test_constant.TD_OLDTIEM)
    test_support.cloud_create_store_file(test_constant.TD_MIDDLE_SAME_2, test_constant.TD_CONTENT_DEFAULT, mock_cloud_db, True, test_constant.TD_OLDTIEM)
    test_support.cloud_create_store_file(test_constant.TD_MIDDLE_DELETE, test_constant.TD_CONTENT_DEFAULT, mock_cloud_db, True, test_constant.TD_OLDTIEM)

    file_support.write_file(test_constant.MOCK_CLOUD_PATH_DB, mock_cloud_db.to_formatted_json_string())
    cloud_file_service.upload_file_by_path(test_constant.MOCK_CLOUD_PATH_DB, mock_cloud_db.get_cloud_db_path())

def trigger():
        # init latest indexs
    latest_index = test_support.build_indexs([
        test_support.build_index(test_constant.TD_MIDDLE_SAME, test_constant.TD_OLDTIEM, True),
        test_support.build_index(test_constant.TD_MIDDLE_CREATE, test_constant.TD_NEWTIME, True),
        test_support.build_index(test_constant.TD_MIDDLE_UPDATE, test_constant.TD_NEWTIME, True),
        test_support.build_index(test_constant.TD_MIDDLE_SAME_2, test_constant.TD_OLDTIEM, True),
    ])
    sync_facade.sync(test_constant.LOCAL_PATH_ROOT, test_constant.CLOUD_PATH_ROOT, test_constant.SWAP_PATH_ROOT, True, test_constant.TD_MODE_MASTER, latest_index)

def check():
    # assert cloud_file_service.is_exist(path_support.merge_path([test_constant.CLOUD_PATH_ROOT, test_constant.TD_MIDDLE_CREATE])) == True
    t1 = encrypter_support.string_source_to_base64_string(test_constant.TD_MIDDLE_CREATE)
    t2 = path_support.merge_path([test_constant.CLOUD_PATH_ROOT, t1])
    cloud_file_service.is_exist(t2)
    assert cloud_file_service.is_exist(path_support.merge_path([test_constant.CLOUD_PATH_ROOT, test_constant.TD_MIDDLE_CREATE_ENCRYPT])) == True
    assert cloud_file_service.is_exist(path_support.merge_path([test_constant.CLOUD_PATH_ROOT, test_constant.TD_MIDDLE_SAME_ENCRYPT])) == True
    assert cloud_file_service.is_exist(path_support.merge_path([test_constant.CLOUD_PATH_ROOT, test_constant.TD_MIDDLE_SAME_2_ENCRYPT])) == True
    assert cloud_file_service.is_exist(path_support.merge_path([test_constant.CLOUD_PATH_ROOT, test_constant.TD_MIDDLE_UPDATE_ENCRYPT])) == True
    assert cloud_file_service.is_exist(path_support.merge_path([test_constant.CLOUD_PATH_ROOT, test_constant.TD_MIDDLE_DELETE_ENCRYPT])) == False

    assert path_support.is_exist(path_support.merge_path([test_constant.LOCAL_PATH_ROOT, test_constant.TD_MIDDLE_CREATE])) == True
    assert path_support.is_exist(path_support.merge_path([test_constant.LOCAL_PATH_ROOT, test_constant.TD_MIDDLE_SAME])) == True
    assert path_support.is_exist(path_support.merge_path([test_constant.LOCAL_PATH_ROOT, test_constant.TD_MIDDLE_SAME_2])) == True
    assert path_support.is_exist(path_support.merge_path([test_constant.LOCAL_PATH_ROOT, test_constant.TD_MIDDLE_UPDATE])) == True
    assert path_support.is_exist(path_support.merge_path([test_constant.LOCAL_PATH_ROOT, test_constant.TD_MIDDLE_DELETE])) == False

    assert cloud_file_service.get_encypt_file_content_by_path(test_constant.CLOUD_PATH_ROOT, test_constant.TD_MIDDLE_UPDATE_ENCRYPT) == test_constant.TD_CONTENT_UPDATE
    '''
    t4 = cloud_file_service.get_file_content_by_path(t3, t1)
    t5 = test_constant.TD_CONTENT_DEFAULT

    t6=encrypter_support.fernet.decrypt(t4)
    t6.decode() == test_constant.TD_CONTENT_DEFAULT


    t3 = test_constant.CLOUD_PATH_ROOT
    bdwp_support.get_file_content_by_path(t3, t1)
    '''




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

    assert local_db_dict[code_file_create][base_file_model.KEY_MTIME] == test_constant.TD_NEWTIME
    assert local_db_dict[code_file_same][base_file_model.KEY_MTIME] == test_constant.TD_OLDTIEM
    assert local_db_dict[code_file_same_2][base_file_model.KEY_MTIME] == test_constant.TD_OLDTIEM
    assert local_db_dict[code_file_update][base_file_model.KEY_MTIME] == test_constant.TD_NEWTIME

    cloud_db_dict = json.loads(cloud_file_service.get_unencypt_file_content_by_path(test_constant.CLOUD_PATH_ROOT, test_constant.BASE_NAME_DB))
    assert len(cloud_db_dict) == 4
    assert code_file_create in cloud_db_dict
    assert code_file_same in cloud_db_dict
    assert code_file_same_2 in cloud_db_dict
    assert code_file_update in cloud_db_dict

    assert cloud_db_dict[code_file_create][base_file_model.KEY_MTIME] == test_constant.TD_NEWTIME
    assert cloud_db_dict[code_file_same][base_file_model.KEY_MTIME] == test_constant.TD_OLDTIEM
    assert cloud_db_dict[code_file_same_2][base_file_model.KEY_MTIME] == test_constant.TD_OLDTIEM
    assert cloud_db_dict[code_file_update][base_file_model.KEY_MTIME] == test_constant.TD_NEWTIME
