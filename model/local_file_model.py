
from model.base_file_model import BaseFileModel
from model.context_model import FolderContext
from support import encrypter_support

class LocalFileModel(BaseFileModel):
    pass

def build_from_file_path(folder_context:FolderContext, local_file_path:str, mtime:str, encrypt:bool):
    unencrypt_middle_path = local_file_path.removeprefix(folder_context.get_local_base_path())

    new_file_model = LocalFileModel(folder_context=folder_context, 
                                    code=encrypter_support.string_hash(unencrypt_middle_path), 
                                    fs_id="", 
                                    file_name=local_file_path.split('/')[-1], 
                                    middle_path=unencrypt_middle_path, 
                                    encrypt=encrypt, 
                                    mtime=mtime)
    # new_file_model.set_folder_context()
    # new_file_model.set_code(encrypter_support.string_hash(unencrypt_middle_path))
    # new_file_model.set_encrypt(encrypt)
    # new_file_model.set_fs_id("")
    # new_file_model.set_mtime(mtime)
    # new_file_model.set_middle_path(unencrypt_middle_path)
    # new_file_model.set_file_name(local_file_path.split('/')[-1])
    return new_file_model
