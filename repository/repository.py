
import json
from model import file_model, context_model
from support import file_support

class FileDB:
    __folder_context: context_model.FolderContext
    __db_context: context_model.DBContext
    __file_dict: dict

    def __init__(self, folder_context:context_model.FolderContext, db_context:context_model.DBContext, db_content_file_path:str):
        self.__folder_context = folder_context
        self.__db_context = db_context
        file_dict_json:dict = json.loads(file_support.read_file_as_string(db_content_file_path))
        for key, value in file_dict_json.items:
            local_file_path = self.__folder_context.get_local_base_path + value[file_model.MIDDLE_PATH_KEY]
            self.__file_dict[key] = file_model.FileModel(self.__folder_context, local_file_path, value[file_model.FS_ID_KEY], value[file_model.ENCRYPT_KEY])

    def get_folder_context(self):
        return self.__folder_context
    def get_db_context(self):
        return self.__db_context
    def get_file_dict(self):
        return self.__file_dict
    def set_folder_context(self, folder_context):
        self.__folder_context = folder_context
    def set_db_context(self, db_context):
        self.__db_context = db_context
    def set_file_dict(self, file_dict):
        self.__file_dict = file_dict

    def file_dict_to_json(self):
        res = {}
        for key in self.__file_dict.keys:
            value: file_model.FileModel = self.__file_dict[key]
            res[key] = value.to_json()
        return res
    
    def update_from_latest_index(self, latest_index: dict):
        for file_code, file_meta in latest_index.items():
            if file_code in self.__file_dict:
                intersation_file_model: file_model.FileModel = self.__file_dict[file_code]
                if file_meta[file_model.LOCAL_MTIME_KEY] != intersation_file_model.get_local_mtime():
                    intersation_file_model.set_local_mtime(file_meta[file_model.LOCAL_MTIME_KEY])
            else:
                local_file_path = self.__folder_context.get_local_base_path()+file_meta[file_model.MIDDLE_PATH_KEY]
                self.__file_dict[file_code] = file_model.FileModel(self.__folder_context, local_file_path, '', file_meta[file_model.ENCRYPT_KEY])

    def get_file_dict_difference(self, to_compare_dict: dict):
        res = {}
        for file_code in self.__file_dict.keys():
            if file_code not in to_compare_dict:
                res[file_code] = self.__file_dict[file_code]
        return res
    
    def get_file_dict_intersation_and_mtime_difference(self, to_compare_dict:dict):
        res = {}
        for file_code in self.__file_dict.keys():
            this_file_model:file_model.FileModel = self.__file_dict[file_code]
            if file_code in to_compare_dict:
                that_file_model:file_model.FileModel = to_compare_dict[file_code]
                if  this_file_model.get_local_mtime() != that_file_model.get_local_mtime():
                    res[file_code] = this_file_model
        return res

    def persistence(self):
        file_dict_json = {}
        for file_code in self.__file_dict.keys():
            a_file_model:file_model.FileModel = self.__file_dict[file_code]
            file_dict_json[file_code] = a_file_model.to_json()
        file_support.write_file(self.__db_context.get_local_db_path(), json.dumps(file_dict_json))

    def remove_file_model(self, key:str):
        del self.__file_dict[key]
