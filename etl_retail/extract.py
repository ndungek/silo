import os
import requests
import pandas as pd
from dotenv import load_dotenv


load_dotenv()  # load variables from .env file

MOCKAROO_API_KEY = os.getenv("MOCKAROO_API_KEY")

# Set paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_PATH = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_PATH, exist_ok=True)

# === CONFIG ===
MOCKAROO_API_KEY = "2b70ba00"  
SCHEMA_NAME = "retail_orders"               
RECORD_COUNT = 1000                         
def fetch_mockaroo_data(schema_name, count, api_key):
    url = f"https://api.mockaroo.com/api/generate.json?key={api_key}&schema={schema_name}&count={count}"
    print(f"🔄 Fetching {count} records from schema '{schema_name}'...")
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    print(f"✅ {len(data)} records fetched.")
    return data

def save_to_file(data, name):
    path = os.path.join(RAW_PATH, f"{name}.json")
    pd.DataFrame(data).to_json(path, orient="records", indent=2)
    print(f"💾 Saved {name} to {path}")

def main():
    data = fetch_mockaroo_data(SCHEMA_NAME, RECORD_COUNT, MOCKAROO_API_KEY)
    save_to_file(data, SCHEMA_NAME)

if __name__ == "__main__":
    main()
