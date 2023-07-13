
def format_folder_path(path:str):
    if path[-1] == '/':
        path += '/'
    return path
