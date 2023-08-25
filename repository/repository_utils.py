
from model import cloud_file_model, local_file_model
from repository import local_repository, cloud_repository


# get file only in cloud DB
# for push, delete in cloud
# for pull, creatw/download in local
def get_file_dict_difference_from_local_repository(source_cloud_repository:cloud_repository.CloudRepository, to_compare_local_repository: local_repository.LocalRepository):
    res:dict = {}
    local_file_dict: dict = to_compare_local_repository.get_file_dict()
    for file_code in source_cloud_repository.get_file_dict().keys():
        if file_code not in local_file_dict:
            difference_file_model:cloud_file_model.CloudFileModel = source_cloud_repository.get_file_dict()[file_code]
            res[file_code] = difference_file_model
    return res

# get file in both local and cloud DB, but timestamp is different
# for push: update in cloud
# for pull: update in local
def get_file_dict_intersation_and_mtime_difference_from_local_repository(source_cloud_repository:cloud_repository.CloudRepository, to_compare_local_repository: local_repository.LocalRepository):
    res:dict = {}
    local_file_dict:dict = to_compare_local_repository.get_file_dict()
    for file_code in source_cloud_repository.get_file_dict().keys():
        if file_code in local_file_dict:
            a_cloud_file_model:cloud_file_model.CloudFileModel = source_cloud_repository.get_file_dict()[file_code]
            a_local_file_model:local_file_model.LocalFileModel = local_file_dict[file_code]
            if  a_cloud_file_model.get_mtime() != a_local_file_model.get_mtime():
                res[file_code] = a_cloud_file_model
    return res

# get file only in local DB
# for push: create in cloud
# for pull: delete in local
def get_file_dict_difference_from_cloud_repository(source_local_repository:local_repository.LocalRepository, to_compare_cloud_repository: cloud_repository.CloudRepository):
    res:dict = {}
    cloud_file_dict: dict = to_compare_cloud_repository.get_file_dict()
    for file_code in source_local_repository.get_file_dict().keys():
        if file_code not in cloud_file_dict:
            difference_file_model:local_file_model.LocalFileModel = source_local_repository.get_file_dict()[file_code]
            res[file_code] = difference_file_model
    return res

# get file in both local and cloud DB, but timestamp is different
# for push: update in cloud 
# for pull: update in local
def get_file_dict_intersation_and_mtime_difference_from_cloud_repository(source_local_repository:local_repository.LocalRepository, to_compare_cloud_repository: cloud_repository.CloudRepository):
    res:dict = {}
    cloud_file_dict:dict = to_compare_cloud_repository.get_file_dict()
    for file_code in source_local_repository.get_file_dict().keys():
        if file_code in cloud_file_dict:
            a_local_file_model:local_file_model.LocalFileModel = source_local_repository.get_file_dict()[file_code]
            a_cloud_file_model:cloud_file_model.CloudFileModel = cloud_file_dict[file_code]
            if  a_local_file_model.get_mtime() != a_cloud_file_model.get_mtime():
                res[file_code] = a_local_file_model
    return res
     