import requests

# ArcGIS credentials (replace with your actual username & password)
username = "magnesyljuasen"
password = "Mosepis96"

# Authentication URL (check if this is the correct one for your server)


# Token request parameters
auth_params = {
    "username": username,
    "password": password,
    "client": "requestip",
    "f": "json"
}

# Get token
auth_response = requests.post(auth_url, data=auth_params)
token = auth_response.json().get("token")

if token:
    print("Token generated successfully:", token)
else:
    print("Failed to generate token:", auth_response.json())