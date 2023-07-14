
from facade import sync_facade
from support.config_support import config

if __name__ == "__main__":
    sync_folder_list = config.get_sync_folder()
    for a_sync_folder in sync_folder_list:
        local_base_path: str = a_sync_folder[config.get_key_local_folder()]
        cloud_base_path: str = a_sync_folder[config.get_key_cloud_folder()]
        swap_base_path:str = a_sync_folder[config.get_swap_folder_path()] + local_base_path.split('/')[-1]
        encrypt: bool = a_sync_folder[config.get_key_encrypt()]
        mode = a_sync_folder[config.get_key_mode()]
        sync_facade.sync(local_base_path, cloud_base_path, swap_base_path, encrypt, mode)