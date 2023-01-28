import requests

token = open("secret/secret.token", "r").read()
# super secret

print(f"prototype 4: get token from login and password")

app_key = open("secret/app_key.token", "r").read()
app_secret = open("secret/app_secret.token", "r").read()

# build the authorization URL:
authorization_url = "https://www.dropbox.com/oauth2/authorize?client_id=%s&response_type=code" % app_key

# send the user to the authorization URL:
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
print(r.text)