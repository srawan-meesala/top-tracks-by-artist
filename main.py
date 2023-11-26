from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf8')

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + auth_base64
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, data=data, headers=headers)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_headers(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_headers(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result)==0:
        print("No Artist Exists.")
        return None
    return json_result[0]

def get_songs(token, artist_id):
    url = "https://api.spotify.com/v1/artists/"
    headers = get_auth_headers(token)
    query = f"{artist_id}/top-tracks?country=IN"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)
    return json_result['tracks']

token = get_token()
name = input("Give me an Artist Name: ")
result = search_for_artist(token, name)
artist_id = result['id']
songs = get_songs(token, artist_id)

for index, song in enumerate(songs):
    print(f"{index+1}.", song['name'])