
from support import path_support

import logging
import time

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def get_logger(logger_name, log_output_path, log_level):
    logger = logging.getLogger(logger_name)
    fh = logging.FileHandler(log_output_path, mode='a+', encoding='utf-8')
    ch = logging.StreamHandler()
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    logger.setLevel(log_level)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

class SyncLogger:
    def __init__(self):
        time_format = time.strftime("%Y%m%d", time.localtime())
        info_log_output_path = './logs/' + time_format +'_info.log'
        if not path_support.is_exist(info_log_output_path):
            path_support.create_override_file(info_log_output_path, "")
        
        self.__info_logger = get_logger("info", info_log_output_path, logging.INFO)
        error_log_output_path = './logs/' + time_format +'_error.log'
        if not path_support.is_exist(error_log_output_path):
            path_support.create_override_file(error_log_output_path, "")
        self.__error_logger = get_logger("error", error_log_output_path, logging.ERROR)
    def info(self, message):
        self.__info_logger.info(message)
    def error(self, message):
        self.__error_logger.error(message)

logger = SyncLogger()
