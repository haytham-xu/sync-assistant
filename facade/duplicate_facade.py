
from service import index_service
from support import path_support

import os
import shutil

def get_duplicate_result(source_folder_path:str, source_rebuild_index:bool, target_folder_path:str, target_rebuild_index:bool):
    source_folder_dict:dict = index_service.get_index_for_folder(source_folder_path, source_rebuild_index)
    target_folder_dict:dict = index_service.get_index_for_folder(target_folder_path, target_rebuild_index)
    source_folder_code_set:set = set(source_folder_dict.keys())
    to_compare_folder_code_set:set = set(target_folder_dict.keys())
    
    to_remove_file_key_set:set = source_folder_code_set.intersection(to_compare_folder_code_set)
    to_move_folder_code_set:set = to_compare_folder_code_set.difference(source_folder_code_set)
    for k in to_remove_file_key_set:
        to_remove_file_path = target_folder_dict[k]
        print("to remove: {}".format(to_remove_file_path))
        # to_remove_file_path = target_folder_dict[k]
        # print("delete: ".format(to_remove_file_path))
        path_support.remove_path(to_remove_file_path)
    for k in to_move_folder_code_set:
        source_file_path:str = target_folder_dict[k]
        middle_path = source_file_path.removeprefix(target_folder_path)
        target_file_path:str = source_folder_path + middle_path
        print("move {} to {}".format(source_file_path, target_file_path))
    # shutil.
    

def remove_deplicate_file(source_folder_path:str, target_folder_path:str, rebuild_index:bool):
    # duplicate_report_path = "./reports/{}-{}-duplicate.json".format()
    # should_move_to_source_report_path = "./reports/{}-{}-move.json".format()
    source_folder_dict:dict = index_service.get_index_for_folder(source_folder_path, rebuild_index)
    target_folder_dict:dict = index_service.get_index_for_folder(target_folder_path, rebuild_index)
    source_folder_code_set:set = set(source_folder_dict.keys())
    to_compare_folder_code_set:set = set(target_folder_dict.keys())
    
    to_remove_file_key_set:set = source_folder_code_set.intersection(to_compare_folder_code_set)
    to_move_folder_code_set:set = to_compare_folder_code_set.difference(source_folder_code_set)
    for k in to_remove_file_key_set:
        to_remove_file_path = target_folder_dict[k]
        print("delete: {}".format(to_remove_file_path))
        path_support.remove_path(to_remove_file_path)
    for k in to_move_folder_code_set:
        source_file_path:str = target_folder_dict[k]
        middle_path = source_file_path.removeprefix(target_folder_path)
        target_file_path:str = source_folder_path + middle_path
        print("move {} to {}".format(source_file_path, target_file_path))
        path_support.move_file_folder(source_file_path, target_file_path)

    # file in dict 1, in dict_2: dulicate --> should remove, report, do nothing for now
    # file in dict 1, not in dict 2: --> that is ok, it should be
    # file not in dict 1, in dict 2: --> report, this should happen as 
