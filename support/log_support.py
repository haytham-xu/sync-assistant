
import logging
import time

# logging.basicConfig(filename='./logs/' + time.strftime("%Y%m%d", time.localtime()) +'.log',
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S',
#     level=logging.INFO,
# )

def log_info(content):
    print_log("--> " + content)

def print_log(content):
    print(content)

