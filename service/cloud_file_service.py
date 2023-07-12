
import os
from support import baiduwangpan
from model import cloud_file_model
# from support.log import logging

def upload_file(file_local_path:str, file_cloud_path:str):
    fs_id = baiduwangpan.upload_file(file_local_path, file_cloud_path)
    # logging.info("%s upload success" % file_local_path)
    return fs_id

def download_file(local_base_path:str, cloud_base_path:str, middle_path:str):
    try:
        res = baiduwangpan.search_file(middle_path, cloud_base_path)
        fs_id = res['list'][0]['fs_id']
        res = baiduwangpan.get_file_meta(fs_id)
        dlink = res['list'][0]['dlink']
        baiduwangpan.download_file(dlink, local_base_path + middle_path)
    except Exception as err:
        raise Exception("Download file Failed: {}".format(err))

def download_file_by_fsid(local_base_path:str, middle_path:str, fs_id:str):
    res = baiduwangpan.get_file_meta(fs_id)
    dlink = res['list'][0]['dlink']
    baiduwangpan.download_file(dlink, local_base_path + middle_path)

def is_file_exist_in_cloud(cloud_file_path:str):
    search_key = cloud_file_path.split('/')[-1]
    search_in = "/".join(cloud_file_path.split('/')[:-1])
    res = baiduwangpan.search_file(search_key, search_in)
    return len(res['list']) != 0

def delete_file_or_folder(cloud_absolute_path:str):
    print("deleting: ", cloud_absolute_path)
    baiduwangpan.delete_file(cloud_absolute_path)

'''
baiduwangpan.get_current_level_file_list
    adv: get file or foler list for only one level, quick and light
    dis: hard to get all files
baiduwangpan.get_multimedia_listall
    adv: this is easier to get all file
    dis: get file and folder list recursion, this may cause two issue:
        even get 1000 file each time, will still need lots of Request.
        file_folder dict in lcoal memory would huge.
'''
def list_folder_file_same_level(target_path):
    limitation = 1000
    current_index = 0
    folder_list = set()
    file_list = set()
    while True:
        res = baiduwangpan.get_current_level_file_list(target_path, 0, current_index, limitation)
        current_file_folder_list = res['list']
        for file_folder in current_file_folder_list:
            if file_folder["isdir"]:
                folder_list.add(file_folder["path"])
            else:
                file_list.add(file_folder["path"])
        current_file_folder_list_length = len(current_file_folder_list)
        if current_file_folder_list_length == 0 or current_file_folder_list_length < limitation:
            break
        current_index += limitation
    return folder_list, file_list


def list_folder_file_recursion(target_path):
    limitation = 1000
    current_index = 0
    file_folder_list = set()
    while True:
        res = baiduwangpan.get_multimedia_listall(target_path, current_index, limitation)
        current_file_folder_list = res['list']
        for file_folder in current_file_folder_list:
            cloud_file_folder_model = cloud_file_model.CloudFileModel()
            cloud_file_folder_model.set_category(file_folder['category'])
            cloud_file_folder_model.set_fs_id(file_folder['fs_id'])
            cloud_file_folder_model.set_is_dir(file_folder['isdir'])
            cloud_file_folder_model.set_local_ctime(file_folder['local_ctime'])
            cloud_file_folder_model.set_local_mtime(file_folder['local_mtime'])
            cloud_file_folder_model.set_md5(file_folder['md5'])
            cloud_file_folder_model.set_path(file_folder['path'])
            cloud_file_folder_model.set_server_ctime(file_folder['server_ctime'])
            cloud_file_folder_model.set_server_filename(file_folder['server_filename'])
            cloud_file_folder_model.set_server_mtime(file_folder['server_mtime'])
            cloud_file_folder_model.set_size(file_folder['size'])
            file_folder_list.add(cloud_file_folder_model)
        current_file_folder_list_length = len(current_file_folder_list)
        if current_file_folder_list_length == 0 or current_file_folder_list_length < limitation:
            break
        current_index += limitation
    return file_folder_list

def get_mtime(path):
    return baiduwangpan.search_file(path.split('/')[-1], '/'.join(path.split('/')[:-1]))['list'][0]['local_mtime']

def upload_file_v2(file_path, local_base_path, cloud_base_path):
    print("uploading file: ", file_path, local_base_path, cloud_base_path)
    file_cloud_path = cloud_base_path + file_path.removeprefix(local_base_path)
    upload_file(file_path, file_cloud_path)

def upload_folder(folder_path, local_base_path, cloud_base_path):
    print("uploading folder: ", folder_path, local_base_path, cloud_base_path)
    for cur_path, _, files in os.walk(folder_path):
        for f in files:
            if f in ['.DS_Store']:
                continue
            print("uploading: ", cur_path + '/' + f)
            upload_file_v2(cur_path + '/' + f, local_base_path, cloud_base_path)
