import sys
# get credits
def get_credits():
  print(sys.argv)
  return sys.argv[0], sys.argv[1] #TODO check if exists

# get operation type
def get_operation_type():
  print(sys.argv)
  return sys.argv[2] #TODO check if exists

# decide where is local path and where is dropbox path
def get_paths(operation_type = "get"):
  #  TODO
   pass

# check if file exists

# try establish connection
# try upload / download file
# display downloading / uploading progress


if __name__ == '__main__':
    print("loading...")
    login, password = get_credits()
    operation_type = get_operation_type()
    # 
    local_path, cloud_path = get_paths(operation_type)


# /////////////////
# trade key-pass to api token
# https://developers.dropbox.com/oauth-guide // ???
# https://www.dropbox.com/developers/reference/auth-types#app
# upload file
# https://www.dropbox.com/developers/documentation/http/documentation#file_requests-create
# download file
# https://www.dropbox.com/developers/documentation/http/documentation#file_requests-get
# https://www.dropbox.com/developers/documentation/http/documentation#files-download