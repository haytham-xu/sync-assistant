
from repository import repository
from model import file_model, context_model
from service import cloud_file_service
from support import path_support, file_support
from uttest import test_constant

def create_store_file(file_path:str, file_content:str, file_db:repository.FileDB, encrypt:bool, local_mtime:str, folder_context: context_model.FolderContext):
    file_support.write_file(file_path, file_content)
    a_file_model = file_model.FileModel(folder_context, file_path, "", encrypt)
    file_db.add_file_by_model(a_file_model)
    file_db.update_file_model_local_mtime_by_code(a_file_model.get_code(), local_mtime)

def clean_test_environment():
    input()
    path_support.remove_path(test_constant.TEST_LOCAL_ROOT_PATH)
    cloud_file_service.delete_file_or_folder(test_constant.TEST_CLOUD_BASE_PATH)