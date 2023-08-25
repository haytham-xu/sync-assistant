
# from model import base_file_model
# from model.context_model import FolderContext
# from model.base_file_model import BaseFileModel
# from support.file_support import read_file_as_string
# from support.path_support import is_exist

# import json

# class BaseRepository:
#     __folder_context: FolderContext
#     __db_name:str
#     __file_dict: dict

#     def __init__(self, folder_context: FolderContext, db_name:str, file_dict: dict):
#         self.__folder_context = folder_context
#         self.__db_name = db_name
#         self.__file_dict = file_dict

    # def file_dict_to_json(self):
    #     res = {}
    #     for key in self.__file_dict.keys():
    #         value: BaseFileModel = self.__file_dict[key]
    #         res[key] = value.to_json()
    #     return res
    
    # def to_formatted_json_string(self):
    #     return json.dumps(self.file_dict_to_json(), indent=4, ensure_ascii=False)

    # def load_from_db_file(self, local_db_file_path:str, file_model):
    #     if not is_exist(local_db_file_path):
    #         return
    #     file_dict_json:dict = json.loads(read_file_as_string(local_db_file_path))
    #     for key, value in file_dict_json.items():
    #         self.__file_dict[key] = file_model(self.__folder_context, 
    #                                                value[base_file_model.KEY_CODE], 
    #                                                value[base_file_model.KEY_FS_ID], 
    #                                                value[base_file_model.KEY_FILE_NAME], 
    #                                                value[base_file_model.KEY_MIDDLE_PATH], 
    #                                                value[base_file_model.KEY_ENCRYPT], 
    #                                                value[base_file_model.KEY_MTIME])
            
    # def remove_file_model(self, key:str):
    #     if key in self.__file_dict:
    #         del self.__file_dict[key]

    # def get_folder_context(self):
    #     return self.__folder_context
    # def get_file_dict(self):
    #     return self.__file_dict
    # def get_db_name(self):
    #     return self.__db_name
