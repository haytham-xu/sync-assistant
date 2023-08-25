
from model.base_file_model import BaseFileModel
from support import encrypter_support
from support import path_support


class CloudFileModel(BaseFileModel):        
    
    def get_local_file_path(self):
        if self.get_encrypt():
            unencrypted_middle_path = '/'.join([encrypter_support.string_base64_to_source_string(p) for p in self.get_middle_path().split('/')])
            return path_support.merge_path([self.get_folder_context().get_local_base_path(), unencrypted_middle_path])
        return path_support.merge_path([self.get_folder_context().get_local_base_path(), self.get_middle_path()])

    def get_cloud_file_path(self):
        return path_support.merge_path([self.get_folder_context().get_cloud_base_path(), self.get_middle_path()])

    def get_swap_file_path(self):
        return path_support.merge_path([self.get_folder_context().get_swap_base_path(), self.get_middle_path()])

    