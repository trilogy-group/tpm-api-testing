import unittest
from playbooks_api import *


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
