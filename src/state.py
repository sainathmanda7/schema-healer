import json

class AgentState:
    def __init__(self):
        self.db_path = 'warehouse.db'
        self.attempted_hashes = set() 
        # Loads the schema dictionary from the project root
        with open("schema_dict.json", "r") as f:
            self.schema_registry = json.load(f)