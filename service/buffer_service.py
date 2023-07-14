
from model import context_model
from support.config_support import config
import os,shutil

def create_buffer_folder(folder_context: context_model.FolderContext):
    os.mkdir(folder_context.get_swap_base_path())
    
def remove_buffer_folder(folder_context: context_model.FolderContext):
    shutil.rmtree(folder_context.get_swap_base_path())
