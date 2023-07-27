
from model import file_model, context_model
from support import file_support, path_support
import json

class FileDB:
    __folder_context: context_model.FolderContext
    __db_context: context_model.DBContext
    __file_dict: dict

    def __init__(self, folder_context:context_model.FolderContext, db_context:context_model.DBContext):
        self.__folder_context = folder_context
        self.__db_context = db_context
        self.__file_dict = {}

    def load_from_db_file(self, existing_db_file_path:str):
        if not path_support.is_exist(existing_db_file_path):
            return
        file_dict_json:dict = json.loads(file_support.read_file_as_string(existing_db_file_path))
        for key, value in file_dict_json.items():
            local_file_path = path_support.merge_path([self.__folder_context.get_local_base_path(), value[file_model.MIDDLE_PATH_KEY]])
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
    
    def file_dict_to_json(self):
        res = {}
        for key in self.__file_dict.keys():
            value: file_model.FileModel = self.__file_dict[key]
            res[key] = value.to_json()
        return res
    
    def to_formatted_json_string(self):
        return json.dumps(self.file_dict_to_json(), indent=4, ensure_ascii=False)

    def persistence(self):
        file_support.write_file(self.__db_context.get_local_db_path(), self.to_formatted_json_string())

    # CRUD for FileModel
    def remove_file_model(self, key:str):
        del self.__file_dict[key]
    def update_file_model_local_mtime_by_code(self, key:str, local_mtime:str):
        target_model:file_model.FileModel = self.__file_dict[key]
        target_model.set_local_mtime(local_mtime)
    def update_file_model_local_mtime_by_model(self, a_file_model: file_model.FileModel, local_mtime:str):
        target_model:file_model.FileModel = self.__file_dict[a_file_model.get_code()]
        target_model.set_local_mtime(local_mtime)
    def add_file_by_path(self, file_path:str, fs_id: str = '', encrypt: bool = False):
        a_file_model = file_model.FileModel(self.__folder_context, file_path, fs_id, encrypt)
        self.add_file_by_model(a_file_model)
    def add_file_by_model(self, a_file_model:file_model.FileModel):
        self.__file_dict[a_file_model.get_code()] = a_file_model
