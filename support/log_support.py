
from model import file_model
import logging, time

# logging.basicConfig(filename='./logs/' + time.strftime("%Y%m%d", time.localtime()) +'.log',
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S',
#     level=logging.INFO,
# )
def log_info(content):
    print_log("--> " + content)

def log_upload_file_success(a_file_model: file_model.FileModel):
    print_log("--> upload success: " + a_file_model.get_middle_path())

def log_delete_local_file_success(a_file_model: file_model.FileModel):
    print_log("--> local delete success: " + a_file_model.get_middle_path())

def print_log(content):
    print(content)

