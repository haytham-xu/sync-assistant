
from model import cloud_file_model
from support import bdwp_support
from support import encrypter_support
from support import path_support

def delete_file_or_folder(cloud_absolute_path:str):
    bdwp_support.delete_file(cloud_absolute_path)

def upload_file(a_file_model:cloud_file_model.CloudFileModel):
    local_file_path = a_file_model.get_local_file_path()
    cloud_file_path = a_file_model.get_cloud_file_path()
    swap_file_path = a_file_model.get_swap_file_path()
    if a_file_model.get_encrypt():
        encrypter_support.file_encrypt(local_file_path, swap_file_path)
        fs_id = upload_file_by_path(swap_file_path, cloud_file_path)
        path_support.remove_path(swap_file_path)
        return fs_id
    return upload_file_by_path(local_file_path, cloud_file_path)

def upload_file_by_path(local_file_path, cloud_file_path):
    return bdwp_support.upload_file(local_file_path, cloud_file_path)

def is_exist(cloud_file_path:str):
    return bdwp_support.is_file_exist_in_cloud(cloud_file_path)

def get_unencypt_file_content_by_path(cloud_base_path:str, middle_path:str):
    byte_content:bytes = bdwp_support.get_file_content_by_path(cloud_base_path, middle_path)
    return byte_content.decode()

def get_encypt_file_content_by_path(cloud_base_path:str, middle_path:str):
    byte_content:bytes = bdwp_support.get_file_content_by_path(cloud_base_path, middle_path)
    byte_content = encrypter_support.data_decrtpt(byte_content.decode())
    return byte_content.decode()

def download_file(a_file_model:cloud_file_model.CloudFileModel):
    local_base_path = a_file_model.get_folder_context().get_local_base_path()
    cloud_base_path = a_file_model.get_folder_context().get_cloud_base_path()
    middle_path = a_file_model.get_middle_path()
    if a_file_model.get_encrypt():
        local_file_path = a_file_model.get_local_file_path()
        swap_base_path = a_file_model.get_folder_context().get_swap_base_path()
        swap_file_path = a_file_model.get_swap_file_path()
        bdwp_support.download_file_with_path(swap_base_path, cloud_base_path, middle_path)
        encrypter_support.file_decrtpt(swap_file_path, local_file_path)
        path_support.remove_path(swap_file_path)
    else:
        bdwp_support.download_file_with_path(local_base_path, cloud_base_path, middle_path)

def clean_empty_cloud():
    pass
