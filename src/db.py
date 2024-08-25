import json
from Accomodation import Accomodation
import os
import time

db_file = "../available.json"
status_file = "../status.json"

class DB:
    """Local representation of available accomodations"""
    
    def get_available_accomodations() -> list:
        
        with open(db_file, "r") as f:
            content = f.read()
        data = json.loads(content)
        return json.loads(content)
    
    def set_available_accomodations(newly_available_accomodations:list):
        
        with open(db_file, "w", encoding="utf-8") as f:
            new_data = json.dumps(newly_available_accomodations)
            f.write(new_data)
    
    def get_last_accomodations_update_time() -> str:
        statbuf = os.stat(db_file)
        last_mod = statbuf.st_mtime
        return time.ctime(last_mod)
    
    def get_accomodations_from_address(name:str) -> str:
        
        data = []
        available_accomodations = DB.get_available_accomodations()
        
        for acc in [Accomodation(acc) for acc in available_accomodations]:
            if re.search(name, acc.address, re.IGNORECASE):
                data.append(acc)
                
        return data
        
        
    def get_program_status() -> bool:
        """true if running, false otherwise"""
        # Check if the file exists
        if not os.path.exists(status_file):
            initial_data = {"running": True}
            with open(status_file, "w") as f:
                json.dump(initial_data, f)
            return initial_data["running"]
        
        # If the file exists, read the status
        try:
            with open(status_file, "r") as f:
                data = json.loads(f.read())
        except json.JSONDecodeError:
            with open(status_file, "w") as f:
                data = {"running": True}
                json.dump(data, f)

        return data["running"]
    
    def set_program_status(new_status:bool):
        
        with open(status_file, "w", encoding="utf-8") as f:
            new_data = {"running": new_status}
            json.dump(new_data, f)
    