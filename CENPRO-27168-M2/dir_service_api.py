import requests, json

endpoint="https://7563sty2tjczbedqhuxd422jny.appsync-api.us-east-1.amazonaws.com/graphql"
api_key="da2-zsihc675pbakbpxet2msxnmpbu"
headers = {"x-api-key": api_key}
calling_app_id="00000000000000000000000001"


def run_query(query):
    
    r = requests.post(endpoint, json={"query": query}, headers=headers)
    if r.status_code == 200:
        response = json.loads(r.text)
        
        if "errors" in response:
            raise Exception(f"Query error", response["errors"])
        return ["data"]
    else:
        raise Exception(f"Query failed to run with a {r.status_code}: {r}")

def list_apps():
    query = '''
        query ListApps {
            listApps(callingAppId: "00000000000000000000000001") {
                id
                name
                metadata {
                properties {
                    format
                    key
                    type
                }
                required
                schema
                searchable
                suggestible
                }
            }
            }
    
    '''.replace("{{calling_app_id}}", calling_app_id)
    return run_query(query)


response = list_apps()
print(response)