import os
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("NSW_API_TOKEN")
RESOURCE_ID = "6095c2b7-8649-4244-902d-4e62c8ea87d9"

def fetch_bus_data(limit=35000) -> pd.DataFrame:
    print("Fetching data from Transport NSW API...")
    url = "https://opendata.transport.nsw.gov.au/api/3/action/datastore_search"
    headers = {"Authorization": API_TOKEN, "Content-Type": "application/json"}
    payload = {"resource_id": RESOURCE_ID, "limit": limit}

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    records = response.json()["result"]["records"]
    df = pd.DataFrame.from_records(records)

    if df.empty:
        print("⚠️ No data found from API.")
        return df

    df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]
    df["trip"] = df["trip"].astype(int)
    df = df.rename(columns={"trip": "trips"})
    df = df.rename(columns={"contract_region": "bus_region"})
    df = df.rename(columns={"_id": "id"})
    df["year_month"] = datetime.now().strftime("%Y-%m")

    # print first few rows for debugging
    print("✅ Data fetched successfully.")

    return df