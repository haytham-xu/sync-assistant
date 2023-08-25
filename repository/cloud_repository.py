
from model import cloud_file_model
from model import local_file_model
from model import context_model
from model import model_mapper
from model import base_file_model
from support import file_support
from support import path_support

import json

class CloudRepository:
    __folder_context: context_model.FolderContext
    __db_name:str
    __file_dict: dict
    __encrypt:bool
    __swap_db_path:str
    __cloud_db_path:str

    def __init__(self, folder_context:context_model.FolderContext, db_name:str, file_dict: dict, encrypt:bool):
        self.__folder_context = folder_context
        self.__db_name = db_name
        self.__file_dict = file_dict
        self.__encrypt = encrypt
        self.__swap_db_path = path_support.merge_path([folder_context.get_swap_base_path(), db_name])
        self.__cloud_db_path = path_support.merge_path([folder_context.get_cloud_base_path(), db_name])

    def persistence(self):
        file_support.write_file(self.get_swap_db_path(), self.to_formatted_json_string())
    def get_swap_db_path(self):
        return self.__swap_db_path
    def get_cloud_db_path(self):
        return self.__cloud_db_path
    
    def get_encrypt(self):
        return self.__encrypt
    def set_encrypt(self, encrypt:bool):
        self.__encrypt = encrypt

    def load_from_cloud_db_file(self, db_file_path:str):
        if not path_support.is_exist(db_file_path):
            return
        file_dict_json:dict = json.loads(file_support.read_file_as_string(db_file_path))
        for key, value in file_dict_json.items():
            self.__file_dict[key] = cloud_file_model.CloudFileModel(self.__folder_context, 
                                                   value[base_file_model.KEY_CODE], 
                                                   value[base_file_model.KEY_FS_ID], 
                                                   value[base_file_model.KEY_FILE_NAME], 
                                                   value[base_file_model.KEY_MIDDLE_PATH], 
                                                   value[base_file_model.KEY_ENCRYPT], 
                                                   value[base_file_model.KEY_MTIME])
    
    def add_file_model_from_cloud_file_model(self, new_cloud_file_model:cloud_file_model.CloudFileModel):
        file_model_key = new_cloud_file_model.get_code()
        if file_model_key in self.get_file_dict():
            raise Exception("file model already exist in file DB.")
        self.__file_dict[file_model_key] = new_cloud_file_model

    def add_file_model_from_local_file_model(self, new_local_file_model:local_file_model.LocalFileModel):
        file_model_key = new_local_file_model.get_code()
        if file_model_key in self.get_file_dict():
            raise Exception("file model already exist in file DB.")
        self.__file_dict[file_model_key] = model_mapper.map_to_cloud_file_model(new_local_file_model)

    def update_mtime_by_key(self, key:str, mtime:str):
        if key not in self.get_file_dict():
            raise Exception("file model not found.")
        existing_file_model: cloud_file_model.CloudFileModel = self.get_file_dict()[key]
        existing_file_model.set_mtime(mtime)

    def file_dict_to_json(self):
        res = {}
        for key in self.__file_dict.keys():
            value: base_file_model.BaseFileModel = self.__file_dict[key]
            res[key] = value.to_json()
        return res
    
    def to_formatted_json_string(self):
        return json.dumps(self.file_dict_to_json(), indent=4, ensure_ascii=False)
            
    def remove_file_model(self, key:str):
        if key in self.__file_dict:
            del self.__file_dict[key]

    def get_folder_context(self):
        return self.__folder_context
    def get_file_dict(self):
        return self.__file_dict
    def get_db_name(self):
        return self.__db_name