import json

def validate_json(file_path):
    """
    Validates the JSON file to ensure it is correctly formatted.

    Args:
        file_path (str): The path to the JSON file to be validated.

    Returns:
        bool: True if the JSON is valid, False otherwise.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        print("JSON is valid")
        return True
    except json.JSONDecodeError as e:
        print(f"JSON error: {e}")
        return False

# example:
validate_json("data/fomc_minutes.json")
