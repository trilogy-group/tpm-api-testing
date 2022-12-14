import requests, time, json, os

#base API url
url="https://h1rejf3su4.execute-api.us-east-1.amazonaws.com/v2"

# Get environment variables
manager_username = os.getenv('manager_username')
manager_pass = os.environ.get('manager_pass')


def get_manager_token():
    
    token = None
    try:
        f = open("token.txt","r")
        token_data =  json.loads(f.read())
        f.close()
        if (token_data["expires"]+3600)>time.time():
            #print("Using previous token")
            return token_data["token"]
    except:    
        print("No token file found")
    
    #print("Extracting token from API")
    base_url="https://imf-api-staging.insidesales.com/v1/users/credentials"
    data={}
    data["username"]=manager_username
    data["password"]=manager_pass

    token_data = requests.post(base_url, json = data).json()
    f = open("token.txt", "w")
    f.write(json.dumps(token_data))
    f.close()
    return token_data["token"]

def generic_get(path):
    token = get_manager_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{url}{path}", headers=headers)
    return response

def generic_post(path, data):
    token = get_manager_token()
    headers = {
        "Authorization": f"Bearer {token}",
        'Content-Type': 'application/json'
        }
    response = requests.post(f"{url}{path}", headers=headers, json=data)
    return response

def generic_patch(path, data):
    token = get_manager_token()
    headers = {
        "Authorization": f"Bearer {token}"
        }
    response = requests.patch(f"{url}{path}", headers=headers, json=data)
    return response

def get_call_paths():  
    response = generic_get("/call-paths")
    return response.json()

def get_specific_path(id):
    return generic_get(f"/call-paths/{id}").json()
    
def get_default_path():
    paths=get_call_paths()
    default_id = paths[0]["id"]
    response = get_specific_path(default_id)
    return response

def create_call_path(name, timezone):
    data={}
    data["name"] = name
    data["time_zone"] = timezone
    
    response = generic_post("/call-paths", data)
    return response.json()

def patch_call_path(id, name, timezone, starting_node="1", nodes = None, edges=None):
    data={}
    data["id"] = 'de957cb2-2502-4927-80cb-11af072fce22'
    data["name"] = name
    data["time_zone"] = timezone
    data["starting_node"]= starting_node
    data["nodes"] = nodes
    data["edges"] = edges

    response = generic_patch(f"/call-paths/{id}", data)
    print(response)
    return response




