
from model import base_file_model
from model import context_model
from support import encrypter_support
from support import path_support

class LocalFileModel(base_file_model.BaseFileModel):
    def get_local_path(self):
        return path_support.merge_path([self.get_folder_context().get_local_base_path(), self.get_middle_path()])

def build_from_file_path(folder_context:context_model.FolderContext, local_file_path:str, mtime:str, encrypt:bool):
    unencrypted_middle_path = local_file_path.removeprefix(folder_context.get_local_base_path())
    print(local_file_path, unencrypted_middle_path)

    new_file_model = LocalFileModel(folder_context=folder_context, 
                                    code=encrypter_support.string_hash(unencrypted_middle_path),
                                    fs_id="", 
                                    file_name=path_support.get_file_folder_name(local_file_path),
                                    middle_path=unencrypted_middle_path,
                                    encrypt=encrypt, 
                                    mtime=mtime)
    return new_file_model
