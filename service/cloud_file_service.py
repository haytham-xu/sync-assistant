
from model import file_model
from support import bdwp_support, encrypter_support

def delete_file_or_folder(cloud_absolute_path:str):
    bdwp_support.delete_file(cloud_absolute_path)

def download_file_by_fsid(a_folder_model:file_model.FileModel):
    res = bdwp_support.get_file_meta(a_folder_model.get_fs_id())
    dlink = res['list'][0]['dlink']
    if not a_folder_model.get_encrypt():
        bdwp_support.download_file(dlink, a_folder_model.get_file_local_path())
        return
    swap_encrypter_file_path = a_folder_model.get_folder_context().get_swap_base_path() + a_folder_model.get_encrypt_middle_path()
    bdwp_support.download_file(dlink, swap_encrypter_file_path)
    encrypter_support.file_decrtpt(swap_encrypter_file_path, a_folder_model.get_file_local_path())

def upload_file(a_folder_model:file_model.FileModel):
    lcoal_file_path = a_folder_model.get_file_local_path()
    cloud_file_path = a_folder_model.get_file_cloud_path()
    if a_folder_model.get_encrypt():
        swap_encrypter_file_path = a_folder_model.get_folder_context().get_swap_base_path() + a_folder_model.get_encrypt_middle_path()
        encrypter_support.file_encrypt(lcoal_file_path, swap_encrypter_file_path)
        lcoal_file_path = swap_encrypter_file_path
        cloud_file_path = a_folder_model.get_file_cloud_path() + a_folder_model.get_encrypt_middle_path()
    fs_id = bdwp_support.upload_file(lcoal_file_path, cloud_file_path)
    return fs_id
