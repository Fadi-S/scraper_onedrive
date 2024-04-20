# Scraper using OneDrive API

This is a simple scraper that uses the OneDrive API to download files from a shared folder. It is written in Python and uses the httpx library to interact with the API.

## Usage
1. Clone the repository `git clone https://github.com/Fadi-S/scraper_onedrive.git`
2. Install the required libraries using `pip install -r requirements.txt`
3. Create a new app in the [Microsoft Entra Portal](https://entra.microsoft.com) and get the client ID, tenant ID and client secret
4. Create keys.json file in the root directory with the same format as keys_example.json and fill in the values
5. Run the script using `python grant_consent.py`
6. Run the script using `python scraper.py`