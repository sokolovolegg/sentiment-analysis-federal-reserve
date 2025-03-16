import json

def check_json_structure(file_path):
    """
    Checks the structure of the JSON file to ensure it contains the required keys.

    Args:
        file_path (str): The path to the JSON file to be checked.

    Returns:
        bool: True if the structure is correct, False otherwise.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        
        # checking that each entry contains the required keys
        for entry in data:
            if not all(key in entry for key in ["filename", "date", "text"]):
                print(f"Error in structure: missing one of the keys in file {entry.get('filename', 'unknown')}")
                return False
        
        print("JSON structure is correct.")
        return True
    except Exception as e:
        print(f"Error checking JSON structure: {e}")
        return False

# example:
check_json_structure("data/fomc_minutes.json")
