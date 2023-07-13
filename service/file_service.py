
from support import baiduwangpan
from support.log import logging
from support.encrypter import encrypter

def upload_file(file_local_path:str, file_cloud_path:str):
    # todo: envrypt?
    fs_id = baiduwangpan.upload_file(file_local_path, file_cloud_path)
    logging.info("%s upload success" % file_local_path)
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

def delete_file(cloud_absolute_path:str):
    baiduwangpan.delete_file(cloud_absolute_path)

def upload_encrypt_file():
    file_encrypt_local_path = local_base_path + encrypt_temp_middle_path + file_encrypt_middle_path
    encrypter.file_encrypt(file_local_path, file_encrypt_local_path)
    file_encrypt_local_md5 = encrypter.get_md5(file_encrypt_local_path)
    fs_id = file_service.upload_file(file_encrypt_local_path, file_encrypt_cloud_path, file_encrypt_local_md5)
    return fs_id
