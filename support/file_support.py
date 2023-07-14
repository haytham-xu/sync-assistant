
def read_file_as_string(file_path):
    res = None
    with open(file_path) as f:
        res = f.read()
    f.close()
    return res

def read_file_as_list(file_path):
    res = None
    with open(file_path) as f:
        res = f.readlines()
    f.close()
    return res

def read_file_as_steam(file_path):
    res = None
    with open(file_path) as f:
        res = f
    f.close()
    return res

def append_file(file_path, append_content):
    with open(file_path, 'a') as f:
        f.write(append_content)
    f.close()

def write_file(file_path:str, content):
    with open(file_path, 'w') as f:
        f.write(content)
    f.close()
