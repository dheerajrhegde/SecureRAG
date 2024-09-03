import streamlit as st

import msal, requests, os

# Configuration
client_id = os.genenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')
tenant_id = os.getenv('AZURE_TENANT_ID')
authority_url = f'https://login.microsoftonline.com/{tenant_id}'
redirect_uri = 'https://securerag-dheeraj.streamlit.app/'
scopes = ['https://graph.microsoft.com/.default']

# Create a confidential client application
app = msal.ConfidentialClientApplication(
    client_id,
    authority=authority_url,
    client_credential=client_secret
)

# Get the authorization URL to redirect the user for sign-in
auth_url = app.get_authorization_request_url(redirect_uri=redirect_uri, scopes=scopes,
                                             response_type='code')

print(f"Please go to this URL and authorize access: {auth_url}")

# After the user logs in and authorizes, they will be redirected to the redirect_uri with a code
# You need to capture the authorization code from the URL query string
# This is a simplified example; in practice, you'd set up a web server to handle this

auth_code = input("Enter the authorization code from the URL: ")

# Exchange the authorization code for an access token
token_response = app.acquire_token_by_authorization_code(auth_code, scopes=scopes, redirect_uri=redirect_uri)

if 'access_token' in token_response:
    access_token = token_response['access_token']
    print("Access token acquired.")
else:
    print(f"Error: {token_response.get('error_description')}")
    exit()

# Construct the URL for the Azure File
file_url = "https://securerag.file.core.windows.net/secure-rag-fs/iphoneQRerror.png"

# Set up the headers with the access token
headers = {
    'Authorization': f'Bearer {access_token}',
    'x-ms-version': '2021-08-06',
    'x-ms-type': 'file',
    'Accept': 'application/json'
}

# Perform the GET request to download the file content
response = requests.get(file_url, headers=headers)

if response.status_code == 200:
    print("Successfully accessed Azure Files!")
    content = response.content
    print(content.decode('utf-8'))  # Assuming the file content is text-based
else:
    print(f"Failed to access Azure Files: {response.status_code} - {response.text}")

