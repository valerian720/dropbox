import sys
import requests
import json
import os

directory_cashed = "cashed"

directory_cashed_app = f"{directory_cashed}/key"
filename_key_app = "app.json"
# 

def get_from_args(key):
  return [item.split('=')[1] for item in sys.argv if item.startswith(f'--{key}=')]
# 

def get_name():
   return get_from_args("name")[0]

def request_new_app_key_secret():
  if not os.path.exists(directory_cashed_app):
    os.makedirs(directory_cashed_app)

  key = input("input app key > ")
  secret = input("input app secret > ")

  data = {"key": key, "secret": secret}
  with open(f"{directory_cashed_app}/{filename_key_app}", 'w') as fp:
    json.dump(data, fp)

  return data

def get_cashed_app_key_secret():
  path = f"{directory_cashed_app}/{filename_key_app}"
  data = None

  if os.path.exists(path):
    with open(path, 'r') as fp:
      data = json.load(fp)
  return data

def get_app_key_secret():
  key_secret = get_cashed_app_key_secret()
  if key_secret is None:
    key_secret = request_new_app_key_secret()
  # 
  return key_secret
# 

def request_new_token():
    key_secret = get_app_key_secret()
    app_key = key_secret["key"]
    app_secret = key_secret["secret"]

    # build the authorization URL:
    authorization_url = "https://www.dropbox.com/oauth2/authorize?client_id=%s&response_type=code" % app_key

    print('Go to the following URL and allow access:')
    print(authorization_url)

    # get the authorization code from the user:
    authorization_code = input('Enter the code:\n')

    # exchange the authorization code for an access token:
    token_url = "https://api.dropboxapi.com/oauth2/token"
    params = {
        "code": authorization_code,
        "grant_type": "authorization_code",
        "client_id": app_key,
        "client_secret": app_secret
    }
    r = requests.post(token_url, data=params)
    print("request_new_token")
    print(r.text)
    token = r.json()["access_token"]
    # 
    path = f"{directory_cashed}/{name}.secret"
    with open(path, 'w') as fp:
      fp.write(token)
    # 
    return token

def get_cashed_token(name):
  path = f"{directory_cashed}/{name}.secret"
  data = ""

  if os.path.exists(path):
    with open(path, 'r') as fp:
      data = fp.read()
  return data

def check_if_token_valid(token):
    domain = "https://api.dropboxapi.com/"
    api_path = "2/files/list_folder"

    url = f"{domain}{api_path}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    body = {"include_deleted": False, "include_has_explicit_shared_members": False, "include_media_info": False,
            "include_mounted_folders": True, "include_non_downloadable_files": True, "path": "", "recursive": False}
    # 
    x = requests.post(url, headers=headers, json=body)
    return not (x.text.startswith("Eror") or ("error" in x.json()))

def get_token(name):
    token = get_cashed_token(name)
    if token == "":
      token = request_new_token()
    # 
    if not check_if_token_valid(token):
       token = request_new_token()
    # 
    return token
# 

def get_operation_type():
  return get_from_args("type")[0] 

def get_paths(operation_type):
  src_path = get_from_args("src_path")[0] 
  dst_path = get_from_args("dst_path")[0] 

  cloud_path = src_path if operation_type == "get" else dst_path
  local_path = src_path if operation_type == "put" else dst_path

  # prep file paths that both of them has file name
  file_name_cloud = cloud_path.split('/').pop()
  file_name_local = local_path.split('/').pop()

  if file_name_cloud == "":
     cloud_path+=file_name_local
  if file_name_local == "":
     local_path+=file_name_cloud
  # 
  # 
  return local_path, cloud_path

# 
def download_file_from_cloud(token, local_path, cloud_path):
  domain = "https://content.dropboxapi.com/"
  api_path = "2/files/download"

  url = f"{domain}{api_path}"
  headers = {
      'Authorization': f'Bearer {token}',
      'Dropbox-API-Arg': json.dumps({"path": cloud_path}), 
  }

  req_result = requests.post(url, headers=headers)
  print("download_file_from_cloud")
  print(req_result.text)

  os.makedirs(os.path.dirname(local_path), exist_ok=True)
  with open(local_path, 'wb') as f:
      f.write(req_result.content)

def upload_file_to_cloud(token, local_path, cloud_path):
  domain = "https://content.dropboxapi.com/"
  api_path = "2/files/upload"

  url = f"{domain}{api_path}"
  headers = {
      'Authorization': f'Bearer {token}',
      'Dropbox-API-Arg': json.dumps({"autorename":False,"mode":"add","mute":False,"path":cloud_path,"strict_conflict":False}), 
      'Content-Type': 'application/octet-stream',
  }

  file = open(local_path,'rb')
  # 
  req_result = requests.post(url, headers=headers, data=file)
  print("upload_file_to_cloud")
  print(req_result.text)

# ///////////////////////////////////////////////////////////////////////////////
# check if this app has cashed app key and secret, if no then request from user
# check if for input username if there is a token and it is valid
#   if no then use Oauth2 to generate token by creating link that allows user to grand abilities to app
# get operation type
# decide where is local path and where is dropbox path
# check if file exists
# try establish connection
# try upload / download file
# display downloading / uploading progress

# py tool.py --name=<username> --type=<put/get> --src_path=<src_path> --dst_path=<dst_path>

# examples
# py tool.py --name=valerian --type=get --src_path=/train.png --dst_path=downloaded/
# py tool.py --name=valerian --type=put --src_path=downloaded/train.png --dst_path=/train_upload.png


if __name__ == '__main__':
  print("loading...")
  # 
  name = get_name()
  # 
  token = get_token(name)
  operation_type = get_operation_type()
  # # 
  local_path, cloud_path = get_paths(operation_type)
  print(f"local_path = {local_path}, cloud_path = {cloud_path}")
  # 
  if operation_type == 'get':
    download_file_from_cloud(token, local_path, cloud_path)
  if operation_type == 'put': 
      upload_file_to_cloud(token, local_path, cloud_path)


# /////////////////
# trade key-pass to api token
# https://developers.dropbox.com/oauth-guide // ???
# https://www.dropbox.com/developers/reference/auth-types#app
# upload file
# https://www.dropbox.com/developers/documentation/http/documentation#file_requests-create
# download file
# https://www.dropbox.com/developers/documentation/http/documentation#file_requests-get
# https://www.dropbox.com/developers/documentation/http/documentation#files-download