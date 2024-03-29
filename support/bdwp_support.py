
from support import config_support
from support import file_support
from support import path_support
import requests
import json
import os
import time
import hashlib

oauth_url = "https://openapi.baidu.com/oauth/2.0/token"
base_url = "https://pan.baidu.com"
http_base_url = "http://pan.baidu.com"
headers = {
  'User-Agent': 'pan.baidu.com'
}
access_token = config_support.config.get_access_token()
refresh_token = config_support.config.get_refresh_token()
app_key = config_support.config.get_app_key()
secret_key = config_support.config.get_secret_key()
bdwp_code = config_support.config.get_bdwp_code()

def http_request(url, method, headers, params={}, payload={}, files={}):
    res = requests.request(method, url, params=params, headers=headers, data = payload, files = files, timeout=360)
    time.sleep(1)
    if res.status_code == 200:
        return res
    raise Exception("Request failed, eror message: ", res.text)

def bdwp_request_with_token(url, method, headers={}, params={}, payload={} ,files=[]):
    params["access_token"] = access_token
    res = http_request(url, method, headers, params, payload ,files)
    json_result = res.json()
    res.close()
    return json_result

def refresh_token():
    params = {"grant_type": "refresh_token", "refresh_token":refresh_token, "client_id":app_key, "client_secret":secret_key}
    res = http_request(oauth_url, "GET", headers, params)
    json_result = res.json()
    res.close()
    return json_result

def get_access_token():
    params = {
        "grant_type": "authorization_code", 
        "code":bdwp_code,
        "client_id":app_key, 
        "client_secret":secret_key,
        "redirect_uri": "oob"
    }
    res = http_request(oauth_url, "GET", headers, params)
    json_result = res.json()
    res.close()
    return json_result

def get_uinfo():
    url = base_url + "/rest/2.0/xpan/nas"
    params = {"method":"uinfo"}
    return bdwp_request_with_token(url, "GET", headers, params)

def get_quota():
    url = base_url + "/api/quota"
    params = {"checkfree": 1, "checkexpire": 1}
    return bdwp_request_with_token(url, "GET", headers, params)

def get_md5(data_string):
    md5 = hashlib.md5()
    md5.update(data_string)
    return md5.hexdigest()

def pre_upload(cloud_path, file_size, md5_list):
    pre_create_url = base_url + "/rest/2.0/xpan/file"
    block_list = json.dumps(md5_list)
    payload = {'path': cloud_path, 'size': file_size, 'block_list': block_list, 'isdir': '0', 'autoinit': '1', 'rtype': '3'}
    params = {"method": "precreate"}
    res = bdwp_request_with_token(pre_create_url, "POST", headers, params, payload)
    upload_id = res['uploadid']
    return upload_id

def upload_chunk(upload_id, chunk_content, chunk_id, cloud_path):
    upload_url = "https://d.pcs.baidu.com/rest/2.0/pcs/superfile2"
    payload = {}
    files = [('file', chunk_content)]
    params = {"path": cloud_path, "uploadid": upload_id, "method": "upload", "type": "tmpfile", "partseq": chunk_id}
    bdwp_request_with_token(upload_url, "POST", headers, params, payload, files)

def create_file(cloud_path, upload_id, md5_list, file_size):
    create_url = base_url + "/rest/2.0/xpan/file"
    block_list = json.dumps(md5_list)
    payload = {'path': cloud_path, 'size': file_size, 'uploadid': upload_id, 'block_list': block_list, 'rtype': '3', 'isdir': '0'}
    params = {"method": "create"}
    res = bdwp_request_with_token(create_url, "POST", headers, params, payload)
    fs_id = res["fs_id"]
    return fs_id

split_size = 50*1024*1024 # MB

def upload_file(file_local_path, target_absolute_path):
    file_size = os.path.getsize(file_local_path)
    file_block = []
    md5_list = []
    with open(file_local_path, 'rb') as f:
        while True:
            chunk = f.read(split_size)
            if not chunk:
                break
            file_block.append(chunk)
        f.close()
    for c in file_block:
        md5_list.append(get_md5(c))
    upload_id = pre_upload(target_absolute_path, file_size, md5_list)
    i = 0
    for c in file_block:
        chunk_content = c
        chunk_id = i
        upload_chunk(upload_id, chunk_content, chunk_id, target_absolute_path)
        i += 1
    return create_file(target_absolute_path, upload_id, md5_list, file_size)

def delete_file(cloud_absolute_path):
    url = base_url + "/rest/2.0/xpan/file"
    params = {"method": "filemanager", "opera": "delete"}
    payload = {"async": "2", "filelist": json.dumps([{'path': cloud_absolute_path}])}
    return bdwp_request_with_token(url, "POST", headers, params, payload)

def get_file_count(cloud_absolute_path):
    res = 0
    for i in range(7):
        res += get_categoryinfo(cloud_absolute_path, i+1)['info'][str(i+1)]['count'] 
    return res

def get_categoryinfo(cloud_absolute_path, category):
    url = base_url + "/api/categoryinfo"
    params = {"category": category, "parent_path": cloud_absolute_path, "recursion": 1}  # category: 1 video、2 music、3 picture、4 document、5 application、6 etc、7 tom
    return bdwp_request_with_token(url, "GET", headers, params)

def create_folder(cloud_absolute_path):
    url = base_url + "/rest/2.0/xpan/file"
    params = {"method": "create"}
    payload = {'path': cloud_absolute_path, 'rtype': '1', 'isdir': '1'}
    return bdwp_request_with_token(url, "POST", headers, params, payload)

def copy_file(cloud_source_file_absolute_path, cloud_target_folder_absolute_path, new_file_name):
    url = base_url + "/rest/2.0/xpan/file"
    params = {"method": "filemanager", "opera": "copy"}
    payload = {"async": "2", "filelist": json.dumps([{'path': cloud_source_file_absolute_path, 'dest': cloud_target_folder_absolute_path, 'newname': new_file_name, 'ondup': 'fail'}])}  # ondup: fail, overwrite
    return bdwp_request_with_token(url, "POST", headers, params, payload)

def get_current_level_file_list(target_cloud_absolute_path, is_only_return_folder=0, start=0, limit=1000):
    url = base_url + "/rest/2.0/xpan/file"
    params = {"dir": target_cloud_absolute_path, "start": start, "limit": limit, "method": "list", "order": "time", "web": 0, "folder": is_only_return_folder, "desc": 1}
    return bdwp_request_with_token(url, "GET", headers, params)

def get_multimedia_listall(target_cloud_absolute_path, start=0, limit=1000):
    url = base_url + "/rest/2.0/xpan/multimedia"
    params = {"method": "listall", "path": target_cloud_absolute_path, "web": 0, "recursion": 1, "start": start, "limit": limit}
    return bdwp_request_with_token(url, "GET", headers, params)

def search_file(search_key, search_in):
    url = base_url + "/rest/2.0/xpan/file"
    params = {"key": search_key, "dir": search_in, "method": "search", "recursion": 1}
    return bdwp_request_with_token(url, "GET", headers, params)

def get_file_meta(file_fsid):
    url = base_url + "/rest/2.0/xpan/multimedia"
    params = {"fsids": json.dumps([file_fsid]), "method": "filemetas", "dlink": 1, "extra": 1, "needmedia": 1}
    return bdwp_request_with_token(url, "GET", headers, params)

def get_file_content_by_path(cloud_base_path:str, middle_path:str):
    res = search_file(middle_path, cloud_base_path)
    fs_id = res['list'][0]['fs_id']
    res = get_file_meta(fs_id)
    dlink = res['list'][0]['dlink']
    return get_file_content(dlink)

def get_file_content(dlink):
    dlink += "&access_token=" + access_token
    res = http_request(dlink, "GET", headers)
    res.close()
    return res.content

def download_file(dlink, local_output_absolute_path):
    file_support.write_file_byte(local_output_absolute_path, get_file_content(dlink))

def download_file_with_path(local_base_path:str, cloud_base_path:str, middle_path:str):
    res = search_file(middle_path, cloud_base_path)
    fs_id = res['list'][0]['fs_id']
    res = get_file_meta(fs_id)
    dlink = res['list'][0]['dlink']
    download_file(dlink, local_base_path + middle_path)

def is_file_exist_in_cloud(cloud_file_path:str):
    search_key = path_support.get_file_folder_name(cloud_file_path)
    parent_path = path_support.get_parent_path(cloud_file_path)
    search_in = path_support.convert_to_unix_path(parent_path)
    res = search_file(search_key, search_in)
    return len(res['list']) != 0

def list_folder_file_same_level(target_path):
    limitation = 1000
    current_index = 0
    folder_list = set()
    file_list = set()
    while True:
        res = get_current_level_file_list(target_path, 0, current_index, limitation)
        current_file_folder_list = res['list']
        for file_folder in current_file_folder_list:
            if file_folder["isdir"]:
                folder_list.add(file_folder)
            else:
                file_list.add(file_folder)
        current_file_folder_list_length = len(current_file_folder_list)
        if current_file_folder_list_length == 0 or current_file_folder_list_length < limitation:
            break
        current_index += limitation
    return folder_list, file_list


def list_folder_file_recursion(target_path):
    limitation = 1000
    current_index = 0
    folder_list = set()
    file_list = set()
    while True:
        res = get_multimedia_listall(target_path, current_index, limitation)
        current_file_folder_list = res['list']
        for file_folder in current_file_folder_list:
            if file_folder["isdir"]:
                folder_list.add(file_folder)
            else:
                file_list.add(file_folder)
        current_file_folder_list_length = len(current_file_folder_list)
        if current_file_folder_list_length == 0 or current_file_folder_list_length < limitation:
            break
        current_index += limitation
    return folder_list, file_list
