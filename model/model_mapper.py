
from model import local_file_model
from model import cloud_file_model
from support import encrypter_support

def map_to_local_file_model(a_cloud_file_model: cloud_file_model.CloudFileModel):
    file_name = ""
    middle_path = ""
    if a_cloud_file_model.get_encrypt():
        file_name = encrypter_support.string_base64_to_source_string(a_cloud_file_model.get_file_name())
        middle_path = '/'.join([encrypter_support.string_base64_to_source_string(p) for p in a_cloud_file_model.get_middle_path().split('/')])
    else:
        file_name = a_cloud_file_model.get_file_name()
        middle_path = a_cloud_file_model.get_middle_path()
    return local_file_model.LocalFileModel(a_cloud_file_model.get_folder_context(),a_cloud_file_model.get_code(), a_cloud_file_model.get_fs_id(), file_name, middle_path, a_cloud_file_model.get_encrypt(), a_cloud_file_model.get_mtime())

def map_to_cloud_file_model(a_local_file_model: local_file_model.LocalFileModel):
    file_name = ""
    middle_path = ""
    if a_local_file_model.get_encrypt():
        file_name = encrypter_support.string_source_to_base64_string(a_local_file_model.get_file_name())
        middle_path = '/'.join([encrypter_support.string_source_to_base64_string(p) for p in a_local_file_model.get_middle_path().split('/')])
    else:
        file_name = a_local_file_model.get_file_name()
        middle_path = a_local_file_model.get_middle_path()
    return cloud_file_model.CloudFileModel(folder_context=a_local_file_model.get_folder_context(),
                                           code=a_local_file_model.get_code(),
                                           fs_id=a_local_file_model.get_fs_id(),
                                           file_name=file_name,
                                           middle_path=middle_path,
                                           encrypt=a_local_file_model.get_encrypt(),
                                           mtime=a_local_file_model.get_mtime())
