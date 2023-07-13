

from service import buffer_service, db_service, index_service
from support import dict_support
from model.local_file_model import FileModel, update_from_quick_index


def sync(local_base_path, cloud_base_path, encrypt, mode):
    # init swap
    buffer_service.create_buffer_folder(local_base_path)
    if mode == "master":
        sync_push(local_base_path, cloud_base_path, encrypt)
    elif mode == "subordinate":
        sync_pull(local_base_path, cloud_base_path, encrypt)
    else:
        raise Exception("Unsupport mode: {}".format(mode))
    # clean swap
    buffer_service.remove_buffer_folder(local_base_path)

def sync_pull(local_base_path, cloud_file_path, encrypt):
    # todo
    pass

def sync_push(local_base_path, cloud_base_path, encrypt):
    # get latest_index
    latest_index_db = index_service.get_latest_local_index(local_base_path)
    # get local_db
    local_db = db_service.read_local_db(local_base_path)
    # download cloud db file to swap
    swap_cloud_db = db_service.read_cloud_db(cloud_base_path)

    need_create_code = set()
    need_update_code = set()
    need_delete_code = set()
    for code in dict_support.get_all_keys([swap_cloud_db, latest_index_db, local_db]):
        if code not in latest_index_db:    # F * *
            need_delete_code.add(code)
        elif code not in local_db:      # T F *
            need_create_code.add(code)
        elif code not in swap_cloud_db:# T T F
            need_create_code.add(code)
        else:                           # T T T
            index_mtime = latest_index_db[code].get_local_mtime()
            local_mtine = local_db[code].get_local_mtime()
            cloud_mtime = swap_cloud_db[code].get_local_mtime()
            if index_mtime == local_mtine and local_mtine == cloud_mtime:
                continue
            need_update_code.add(code)

    handle_create(need_create_code, latest_index_db, local_db, swap_cloud_db, encrypt)
    handle_update(need_update_code, latest_index_db, local_db, swap_cloud_db, encrypt)
    handle_delete(need_delete_code, latest_index_db, local_db, swap_cloud_db)
    # compare local_db with latest_index, cloud_db, get need_create, need_update, need_delete
    # operator need_update, update cloud_db
    # operator need_delete, update cloud_db

def handle_create(need_create_code, latest_index_db, local_db, swap_cloud_db, encrypt):
    for code in need_create_code:
        local_db[code] = update_from_quick_index(local_db[code], latest_index_db[code])
        # todo

def handle_update(need_update_code, latest_index_db, local_db, swap_cloud_db, encrypt):
    pass

def handle_delete(need_delete_code, latest_index_db, local_db, swap_cloud_db):
    pass

def update_db(latest_index_db, local_db, swap_cloud_db):
    pass

# def sync_push(local_base_path, cloud_base_path, encrypt):
#     print("--> ", local_base_path)
#     print("--> ", cloud_base_path)
#     local_folder = set()
#     local_file = set()
#     cloud_folder = set()
#     cloud_file = set()
#     need_update_file = set()
#     need_update_folder = set()
#     need_delete_file = set()
#     need_delete_folder = set()
#     current_local_path = local_base_path
#     currnt_cloud_path = cloud_base_path
#     while True:
#         cloud_folder, cloud_file = cloud_file_service.list_folder_file_same_level(currnt_cloud_path)
#         local_folder, local_file = filefolder.list_folder_file(current_local_path)
#         cloud_folder = {absolute_path.removeprefix(cloud_base_path) + '/' for absolute_path in cloud_folder}
#         cloud_file = {absolute_path.removeprefix(cloud_base_path) for absolute_path in cloud_file}
#         local_folder = {absolute_path.removeprefix(local_base_path) for absolute_path in local_folder}
#         local_file = {absolute_path.removeprefix(local_base_path) for absolute_path in local_file}

#         need_update_file_set = local_file.difference(cloud_file)
#         need_delete_file_set = cloud_file.difference(local_file)
#         need_update_file.update(need_update_file_set)
#         need_delete_file.update(need_delete_file_set)
#         local_file.difference_update(need_update_file_set)
#         cloud_file.difference_update(need_delete_file_set)

#         need_update_folder_set = local_folder.difference(cloud_folder)
#         need_delete_folder_set = cloud_folder.difference(local_folder)
#         need_update_folder.update(need_update_folder_set)
#         need_delete_folder.update(need_delete_folder_set)
#         local_folder.difference_update(need_update_folder_set)
#         cloud_folder.difference_update(need_delete_folder_set)

#         buffer_set = set()
#         for f in local_file:
#             buffer_set.add(f)
#             local_mtime = filefolder.get_mtime(local_base_path + f)
#             cloud_mtime = cloud_file_service.get_mtime(cloud_base_path + f)
#             if local_mtime != cloud_mtime:
#                 print("--> ", f, local_mtime, cloud_mtime)
#                 need_update_file.add(f)
#         local_file.difference_update(buffer_set)
#         cloud_file.difference_update(buffer_set)

#         if len(local_folder) == 0 and len(cloud_folder) == 0:
#             break
#         next_path = list(local_folder)[0]
#         current_local_path = local_base_path + next_path
#         currnt_cloud_path = cloud_base_path + next_path
#         local_folder.remove(next_path)
#         cloud_folder.remove(next_path)
#         # break
#     print("~~~~")
#     print("--> should upload file: ", need_update_file)
#     print("--> should delete file: ", need_delete_file)
#     print("--> should upload folder: ", need_update_folder)
#     print("--> should delete folder: ", need_delete_folder)
#     for f in need_delete_file:
#         cloud_file_service.delete_file_or_folder(cloud_base_path + f)
#     for f in need_delete_folder:
#         cloud_file_service.delete_file_or_folder(cloud_base_path + f)
#     for f in need_update_file:
#         cloud_file_service.upload_file_v2(local_base_path + f, local_base_path, cloud_base_path)
#     for f in need_update_folder:
#         cloud_file_service.upload_folder(local_base_path + f, local_base_path, cloud_base_path)




    # print("hi: ", baiduwangpan.get_uinfo())
    # baiduwangpan.refresh_token()
    # cloud_file_service.list_folder("/apps/sync-assistant/Warehouse/")
    # filefolder