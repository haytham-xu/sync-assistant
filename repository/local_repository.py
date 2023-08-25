

# from repository.base_repository import BaseRepository
# from repository.cloud_repository import CloudRepository
from model import base_file_model
from model import local_file_model
from model import cloud_file_model
from model import model_mapper
from model import context_model

from support import path_support
from support import file_support

from model import base_file_model
from model.context_model import FolderContext
from model.base_file_model import BaseFileModel
from support.file_support import read_file_as_string
from support.path_support import is_exist

import json

class LocalRepository:
    __folder_context: FolderContext
    __db_name:str
    __file_dict: dict

    __local_db_path: str

    def __init__(self, folder_context: context_model.FolderContext, db_name:str, file_dict: dict):
        # super().__init__(folder_context, db_name, file_dict)
        self.__folder_context = folder_context
        self.__db_name = db_name
        self.__file_dict = file_dict
        self.__local_db_path = path_support.merge_path([folder_context.get_local_base_path(), db_name])

    def persistence(self):
        file_support.write_file(self.get_db_path(), self.to_formatted_json_string())
        
    def get_db_path(self):
        return self.__local_db_path

    def load_from_local_db_file(self, db_file_path:str):
        if not is_exist(db_file_path):
            return
        file_dict_json:dict = json.loads(read_file_as_string(db_file_path))
        for key, value in file_dict_json.items():
            self.__file_dict[key] = local_file_model.LocalFileModel(self.__folder_context, 
                                                   value[base_file_model.KEY_CODE], 
                                                   value[base_file_model.KEY_FS_ID], 
                                                   value[base_file_model.KEY_FILE_NAME], 
                                                   value[base_file_model.KEY_MIDDLE_PATH], 
                                                   value[base_file_model.KEY_ENCRYPT], 
                                                   value[base_file_model.KEY_MTIME])
        # self.load_from_db_file(local_db_file_path, local_file_model.LocalFileModel)
        
    def update_from_latest_index(self, latest_index: dict):
        for file_code, file_meta in latest_index.items():
            if file_code in self.__file_dict:
                intersation_file_model: local_file_model.LocalFileModel = self.__file_dict[file_code]
                if file_meta[base_file_model.KEY_MTIME] != intersation_file_model.get_mtime():
                    intersation_file_model.set_mtime(file_meta[base_file_model.KEY_MTIME])
            else:
                local_file_path = path_support.merge_path([self.__folder_context.get_local_base_path(), file_meta[base_file_model.KEY_MIDDLE_PATH]])
                self.__file_dict[file_code] = local_file_model.build_from_file_path(self.__folder_context, 
                                                                                    local_file_path, 
                                                                                    file_meta[base_file_model.KEY_MTIME],
                                                                                    file_meta[base_file_model.KEY_ENCRYPT])
    
    # get file only in local DB
    # for push: create in cloud
    # for pull: delete in local
    # def get_file_dict_difference(self, to_compare_cloud_repository: CloudRepository):
    #     res:dict = {}
    #     cloud_file_dict: dict = to_compare_cloud_repository.get_file_dict()
    #     for file_code in self.__file_dict.keys():
    #         if file_code not in cloud_file_dict:
    #             difference_file_model:local_file_model.LocalFileModel = self.__file_dict[file_code]
    #             res[file_code] = difference_file_model
    #     return res
    
    # get file in both local and cloud DB, but timestamp is different
    # for push: update in cloud 
    # for pull: update in local
    # def get_file_dict_intersation_and_mtime_difference(self, to_compare_cloud_repository: CloudRepository):
    #     res:dict = {}
    #     cloud_file_dict:dict = to_compare_cloud_repository.get_file_dict()
    #     for file_code in self.__file_dict.keys():
    #         if file_code in cloud_file_dict:
    #             a_local_file_model:local_file_model.LocalFileModel = self.__file_dict[file_code]
    #             a_cloud_file_model:cloud_file_model.CloudFileModel = cloud_file_dict[file_code]
    #             if  a_local_file_model.get_mtime() != a_cloud_file_model.get_mtime():
    #                 res[file_code] = a_local_file_model
    #     return res
    
    def add_file_model_from_local_file_model(self, new_local_file_model:local_file_model.LocalFileModel):
        file_model_key = new_local_file_model.get_code()
        if file_model_key in self.get_file_dict():
            raise Exception("file model already exist in file DB.")
        self.__file_dict[file_model_key] = new_local_file_model
    
    def add_file_model_from_cloud_file_model(self, new_cloud_file_model:cloud_file_model.CloudFileModel):
        file_model_key = new_cloud_file_model.get_code()
        if file_model_key in self.get_file_dict():
            raise Exception("file model already exist in file DB.")
        self.__file_dict[file_model_key] = model_mapper.map_to_local_file_model(new_cloud_file_model)


    def update_mtime_by_key(self, key:str, mtime:str):
        if key not in self.get_file_dict():
            raise Exception("file model not found.")
        existing_file_model: cloud_file_model.CloudFileModel = self.get_file_dict()[key]
        existing_file_model.set_mtime(mtime)


    def file_dict_to_json(self):
        res = {}
        for key in self.__file_dict.keys():
            value: BaseFileModel = self.__file_dict[key]
            res[key] = value.to_json()
        return res
    
    def to_formatted_json_string(self):
        return json.dumps(self.file_dict_to_json(), indent=4, ensure_ascii=False)

    # def load_from_db_file(self, local_db_file_path:str, file_model):

            
    def remove_file_model(self, key:str):
        if key in self.__file_dict:
            del self.__file_dict[key]

    def get_folder_context(self):
        return self.__folder_context
    def get_file_dict(self):
        return self.__file_dict
    def get_db_name(self):
        return self.__db_name