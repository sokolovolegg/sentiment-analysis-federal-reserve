import requests
from bs4 import BeautifulSoup
import os
import time  

# Generate a list of all dates for the links
years = list(range(2024, 1999, -1))  # in range from 2024 to 2000 (inclusive)
months = list(range(1, 13))  
days = list(range(1, 32))  

def generate_url(year, month, day):
    """
    Generate the URL for the FOMC minutes for a given date.

    Args:
        year (int): The year of the minutes.
        month (int): The month of the minutes.
        day (int): The day of the minutes.

    Returns:
        str: The formatted URL for the FOMC minutes.
    """
    # here months and days are formatted with leading zeros
    month_str = str(month).zfill(2)
    day_str = str(day).zfill(2)
    return f"https://www.federalreserve.gov/fomc/minutes/{year}{month_str}{day_str}.htm"

# creating a folder to store the texts
os.makedirs("fomc_minutes", exist_ok=True)

# trying each page for all combinations
for year in years:
    for month in months:
        for day in days:
            url = generate_url(year, month, day)
            print(f"Attempting to load page: {url}")
            
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Error loading page {url}: {response.status_code}")
                continue
            
            # parsing the html page
            soup = BeautifulSoup(response.text, "html.parser")
            
            # extracting the text
            text = soup.get_text(separator="\n", strip=True)
            
            # filename for saving
            filename = url.split("/")[-1].replace(".htm", ".txt") 
            filepath = os.path.join("fomc_minutes", filename)
            
            # saving the text to a .txt file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)
            
            print(f"Saved: {filename}")
            
            # adding a delay to avoid overloading the server, also possible with a random delay in range 1 - 3, to make it more natural
            time.sleep(1)  # 1 second delay
