import requests

token = open("secret.token", "r").read()
# super secret

print(f"prototype 4: get token from login and password")
#
# domain = "https://api.dropboxapi.com/"
# api_path = "2/files/list_folder"

# url = f"{domain}{api_path}"
# headers = {
#     'Authorization': f'Bearer {token}',
#     'Content-Type': 'application/json',
# }

# body = {"include_deleted": False, "include_has_explicit_shared_members": False, "include_media_info": False,
#         "include_mounted_folders": True, "include_non_downloadable_files": True, "path": "", "recursive": False}

# # curl -X POST https://api.dropboxapi.com/2/files/list_folder \
# # --header "Authorization: Bearer <token>" \
# # --header "Content-Type: application/json" \
# # --data "{\"include_deleted\":false,\"include_has_explicit_shared_members\":false,\"include_media_info\":false,\"include_mounted_folders\":true,\"include_non_downloadable_files\":true,\"path\":\"/Homework/math\",\"recursive\":false}"
# #
# x = requests.post(url, headers=headers, json=body)
# print(x.text)
