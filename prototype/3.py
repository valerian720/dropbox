import requests
import json

token = open("secret/secret.token", "r").read()
# super secret

print(f"prototype 3: upload test2.txt")
#
source_folder = "downloaded/test2.txt"
# source_folder = "downloaded/train2.png"

target_folder = "/new_folder/"
#
domain = "https://content.dropboxapi.com/"
api_path = "2/files/upload"

url = f"{domain}{api_path}"
target_filename = source_folder.split('/').pop()
headers = {
    'Authorization': f'Bearer {token}',
    'Dropbox-API-Arg': json.dumps({"autorename":False,"mode":"add","mute":False,"path":target_folder+target_filename,"strict_conflict":False}), 
    'Content-Type': 'application/octet-stream',
}

file = open(source_folder,'rb')

# curl -X POST https://content.dropboxapi.com/2/files/upload \
#     --header "Authorization: Bearer <get access token>" \
#     --header "Dropbox-API-Arg: {\"autorename\":false,\"mode\":\"add\",\"mute\":false,\"path\":\"/Homework/math/Matrices.txt\",\"strict_conflict\":false}" \
#     --header "Content-Type: application/octet-stream" \
#     --data-binary @local_file.txt


req_result = requests.post(url, headers=headers, data=file)
print(req_result.text)

# https://www.dropbox.com/developers/