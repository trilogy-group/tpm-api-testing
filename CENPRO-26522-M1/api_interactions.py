import requests
import time
import json

url="https://h1rejf3su4.execute-api.us-east-1.amazonaws.com/v2"

def get_manager_token():
    
    token = None
    try:
        f = open("token.txt","r")
        token_data =  json.loads(f.read())
        f.close()
        if token_data["expires"]>time.time():
            print("Using previous token")
            return token_data["token"]
    except:    
        print("No token file found")
    
    print("Extracting token from API")
    base_url="https://imf-api-staging.insidesales.com/v1/users/credentials"
    data={}
    data["username"]="insidesales.leads+canarym@trilogy.com"
    data["password"]="insidesales2manager"

    response = requests.post(base_url, json = data)
    f = open("token.txt", "w")
    f.write(json.dumps(response.json()))
    f.close()
    return response.json()["token"]

def generic_get(path):
    token = get_manager_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{url}{path}", headers=headers)
    return response

def get_call_paths():  
    response = generic_get("/call-paths")
    return response.json()

def get_default_path():
    paths=get_call_paths()
    default_id = paths[0]["id"]
    response = generic_get(f"/call-paths/{default_id}")
    print(response.json())

get_default_path()

