import requests
import json

token = open("secret.token", "r").read()
# super secret

print(f"prototype 2: download test.txt")
#
source_folder = "/test.txt"
# source_folder = "/train.png"

target_folder = "downloaded"
#
domain = "https://content.dropboxapi.com/"
api_path = "2/files/download"

url = f"{domain}{api_path}"
headers = {
    'Authorization': f'Bearer {token}',
    'Dropbox-API-Arg': json.dumps({"path": source_folder}), 
}


# curl -X POST https://content.dropboxapi.com/2/files/download \
#     --header "Authorization: Bearer <get access token>" \
#     --header "Dropbox-API-Arg: {\"path\":\"/Homework/math/Prime_Numbers.txt\"}"
# 
req_result = requests.post(url, headers=headers)
print(req_result.text)

with open(f"{target_folder}{source_folder}", 'wb') as f:
    f.write(req_result.content)