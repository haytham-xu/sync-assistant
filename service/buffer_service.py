
from support.config import config
import os,shutil

def create_buffer_folder(buffer_base_path:str):
    if not os.path.exists(config.get_swap_folder_path()):
        os.mkdir(config.get_swap_folder_path())
    if not os.path.exists(buffer_base_path):
        os.mkdir(buffer_base_path)
    
def remove_buffer_folder():
    shutil.rmtree(config.get_swap_folder_path())

    
