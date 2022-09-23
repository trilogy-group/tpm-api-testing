import requests, time, json, os, unittest

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

class TestSum(unittest.TestCase):

    def test_default_path(self):
        path = get_default_path() 
        assert "id" in path, "Path object should contain `id` field"
        assert "nodes" in path, "Path should contain nodes"
        assert len(path["nodes"])>1, "Should have at least 2 nodes"

    def test_list_path(self):
        paths = get_call_paths()     
        assert type(paths) is list, "Should return an array of Paths"
        print("got list of ", len(paths), "paths")
        for path in paths:
            if path["is_default"]:
                assert path["inbound_numbers"]==[], "Inbound numbers should be empty"

    def test_create_path(self):
        path_data = create_call_path("chris-path", "UTC")
        assert "id" in path_data, "Path creation should return a path ID"
        id = path_data["id"]
        
        path = get_specific_path(id)
        print("Created path", path)
        assert path["is_default"]==False, "Path should not be the default"

    def test_patch_path(self):
        id = "1bb464d1-3367-4d11-8645-9ab6307913e8"
        edges = [{'start': '1', 'end': '2', 'edge_type': 'default'}]
        nodes = [{'id': '1', 'node_type': 'route_to_last_caller', 'record_search_type': 'lead', 'no_answer_failover_type': 'general', 'agent_answer_timeout': 60, 'called_within_days': 30}, {'id': '2', 'node_type': 'forward', 'caller_id_display_type': 'caller'}]

        response = patch_call_path(id, "chris-path2", "UTC", nodes=nodes, edges = edges)
        

if __name__ == "__main__":
    unittest.main()



