
from model import file_model
from support import bdwp_support, encrypter_support, path_support

def delete_file_or_folder(cloud_absolute_path:str):
    bdwp_support.delete_file(cloud_absolute_path)

def download_file_by_fsid(a_folder_model:file_model.FileModel):
    res = bdwp_support.get_file_meta(a_folder_model.get_fs_id())
    dlink = res['list'][0]['dlink']
    if not a_folder_model.get_encrypt():
        bdwp_support.download_file(dlink, a_folder_model.get_file_local_path())
        return
    swap_encrypter_file_path = path_support.merge_path([a_folder_model.get_folder_context().get_swap_base_path(), a_folder_model.get_middle_path()])
    bdwp_support.download_file(dlink, swap_encrypter_file_path)
    encrypter_support.file_decrtpt(swap_encrypter_file_path, a_folder_model.get_file_local_path())

def upload_file(a_file_model:file_model.FileModel):
    local_file_path = a_file_model.get_file_local_path()
    cloud_file_path = a_file_model.get_file_cloud_path()
    if a_file_model.get_encrypt():
        swap_file_path = a_file_model.get_file_swap_path()
        encrypter_support.file_encrypt(local_file_path, swap_file_path)
        local_file_path = swap_file_path
        # swap_encrypter_file_path = path_support.merge_path([a_file_model.get_folder_context().get_swap_base_path(), a_file_model.get_middle_path()])
        # cloud_encrypter_file_path = path_support.merge_path([a_file_model.get_file_cloud_path(), a_file_model.get_middle_path()])
        # return upload_encryot_file(local_file_path, swap_encrypter_file_path, cloud_encrypter_file_path)
    return upload_file_by_path(local_file_path, cloud_file_path)

def upload_file_by_path(local_file_path, cloud_file_path):
    return bdwp_support.upload_file(local_file_path, cloud_file_path) # fs_id

# def upload_encryot_file(local_file_path, swap_encrypter_file_path, cloud_encrypter_file_path):
#     encrypter_support.file_encrypt(local_file_path, swap_encrypter_file_path)
#     return bdwp_support.upload_file(swap_encrypter_file_path, cloud_encrypter_file_path) # fs_id

def is_exist(cloud_file_path:str):
    return bdwp_support.is_file_exist_in_cloud(cloud_file_path)

def get_file_content(file_model:file_model.FileModel):
    return get_file_content_by_path(file_model.get_folder_context().get_cloud_base_path(), file_model.get_middle_path())

def get_file_content_by_path(cloud_base_path:str, middle_path:str):
    byte_content:bytes = bdwp_support.get_file_content_by_path(cloud_base_path, middle_path)
    return byte_content.decode()
