import os

directory = "data/raw/fomc_minutes"
processed_directory = "data/processed/fomc_minutes"

# The main text begins differently before and after 2010, so we need different start phrases
# and the same end phrases for both periods
start_phrases = {
    "2000-2009": "The information",
    "2010-2024": "Staff Review of the Economic Situation"
}
end_phrases = ["Voting for this action", "Votes for this action"]

# creating a folder for processed files if it doesn't exist
os.makedirs(processed_directory, exist_ok=True)

def trim_file(filepath, start_phrase):
    """
    Trims the content of a file based on the given phrases. Only the content without member names is needed.

    Args:
        filepath (str): The path to the file to be trimmed.
        start_phrase (str): The phrase indicating the start of the relevant content.

    Returns:
        str: The trimmed content if both start and end phrases are found, otherwise None.
    """
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    start_index = content.find(start_phrase)
    end_index = min((content.find(phrase) for phrase in end_phrases if content.find(phrase) != -1), default=-1)

    if start_index != -1 and end_index != -1:
        trimmed_content = content[start_index:end_index]
        return trimmed_content.strip()
    
    return None  # if there is no phrases found

# processing files
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    
    if os.path.isfile(filepath) and filename.lower().startswith("fomcminutes"):
        try:
            year = int(filename[11:15])  # extracting the year
            if 2000 <= year <= 2009:
                start_phrase = start_phrases["2000-2009"] # applying the first start phrase
            elif 2010 <= year <= 2024:
                start_phrase = start_phrases["2010-2024"] # applying the second start phrase
            else:
                continue  # skip files with years outside the range

            trimmed_content = trim_file(filepath, start_phrase)
            if trimmed_content:
                trimmed_filepath = os.path.join(processed_directory, filename)
                with open(trimmed_filepath, "w", encoding="utf-8") as file:
                    file.write(trimmed_content)

        except ValueError:
            print(f"Error: Could not determine the year for file {filename}")

print("Trimming completed. All processed files are saved in 'data/processed/fomc_minutes'.")
