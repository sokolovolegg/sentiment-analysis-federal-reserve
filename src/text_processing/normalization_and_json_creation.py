import os
import json
import re

processed_directory = "data/processed/fomc_minutes"
output_json = "data/fomc_minutes.json"

def normalize_text(text):
    """
    Removes extra spaces, empty lines, fixes strange characters, and normalizes the text.

    Args:
        text (str): The text to be normalized.

    Returns:
        str: The normalized text.
    """

    text = text.replace("ï¿½", "")  # such characters appear due to incorrect encoding
    
    # all sequences of spaces and new lines with a single space are replaced
    text = re.sub(r'\s+', ' ', text)
    
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)  # removing control characters (ASCII < 32)

    return text.strip()

data = []

# read files
for filename in os.listdir(processed_directory):
    filepath = os.path.join(processed_directory, filename)
    if os.path.isfile(filepath) and filename.lower().startswith("fomcminutes"):
        
        # extract date from the filename
        date_str = filename[11:19]  # YYYYMMDD format
        date_formatted = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}";  # YYYY-MM-DD
        
        with open(filepath, "r", encoding="utf-8") as file:
            text = file.read()
            normalized_text = normalize_text(text)
        
        data.append({
            "filename": filename,
            "date": date_formatted,
            "text": normalized_text
        })

# saving to JSON
with open(output_json, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"JSON saved to {output_json}")

