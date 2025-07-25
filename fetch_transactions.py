import requests
import pandas as pd
import json
import os
from dotenv import load_dotenv 


load_dotenv()

API_KEY = os.getenv("COVALENT_API_KEY")
BASE_URL = "https://api.covalenthq.com/v1/1/address/{wallet}/transactions_v2/?key={api_key}"


# Load wallet addresses
wallet_df = pd.read_csv("data/wallets.csv")
wallets = wallet_df['wallet_id'].tolist()

raw_data = {}

def fetch_transactions(wallet):
    """Fetch transaction history for a given wallet."""
    url = BASE_URL.format(wallet=wallet, api_key=API_KEY)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching {wallet}: {response.status_code}")
        return None

for wallet in wallets:
    print(f"Fetching transactions for: {wallet}")
    data = fetch_transactions(wallet)
    if data:
        raw_data[wallet] = data

# Save raw transaction data
with open("data/raw_transactions.json", "w") as f:
    json.dump(raw_data, f, indent=2)

print(f"✅ Data for {len(raw_data)} wallets saved to data/raw_transactions.json")