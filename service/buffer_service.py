
from support.config import config
import os,shutil

def create_buffer_folder(local_base_path:str):
    if not os.path.exists(config.get_swap_folder_path()):
        os.mkdir(config.get_swap_folder_path())
    folder_name = local_base_path.split('/')[-1]
    swap_path = config.get_swap_folder_path() + folder_name
    if not os.path.exists(swap_path):
        os.mkdir(swap_path)
    
def remove_buffer_folder(local_base_path:str):
    folder_name = local_base_path.split('/')[-1]
    swap_path = config.get_swap_folder_path() + folder_name
    shutil.rmtree(swap_path)

    
