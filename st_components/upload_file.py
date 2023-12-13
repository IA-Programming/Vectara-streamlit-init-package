import streamlit as st
import requests

from urllib.parse import urlencode

# https://github.com/homanmirgolbabaee/ragtag-code-jammer/blob/main/app.py

def get_vectara_jwt(client_id, client_secret, auth_url):
    # The data to be sent with the POST request
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    # Sending a POST request to retrieve the JWT token
    response = requests.post(auth_url, data=urlencode(data), headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the token from the response
        jwt_token = response.json().get('access_token')
        return jwt_token
    else:
        raise Exception(f"Error retrieving JWT token: {response.text}")
    
def upload_file_to_vectara(file,doc_metadata):
    VECTARA_UPLOAD_ENDPOINT = "https://api.vectara.io/v1/upload"
    customer_id = st.secrets['CUSTOMER_ID']
    corpus_id = st.secrets['CORPUS_ID']
    client_id = st.secrets['client_id']
    client_secret = st.secrets['client_secret']
    auth_url = st.secrets['auth_url']

    jwt_token = get_vectara_jwt(client_id, client_secret, auth_url)
    jwt_token = str(jwt_token)
    #jwt_token = os.getenv('VECTARA_JWT')  # Add your JWT token to your .env file

    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'grpc-timeout': '30S'
    }
    
    files = {
        'file': (file.name, file, 'application/octet-stream'),
        'doc_metadata': (None, doc_metadata, 'application/json')
    }
    
    params = {
        'c': customer_id,
        'o': corpus_id,
    }
    
    try:
        response = requests.post(VECTARA_UPLOAD_ENDPOINT, headers=headers, files=files, params=params)
        if response.status_code == 200:
            return {"success": True, "message": "File uploaded successfully!"}
        else:
            return {"success": False, "message": response.text}
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": str(e)}