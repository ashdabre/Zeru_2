import json
import csv
import os

# File paths
RAW_DATA_FILE = 'data/raw_transactions.json'
PROCESSED_FILE = 'data/processed_data.csv'

def load_raw_data():
    """Load raw JSON data from the raw file."""
    if not os.path.exists(RAW_DATA_FILE):
        print(f"❌ Raw data file {RAW_DATA_FILE} not found.")
        return {}
    with open(RAW_DATA_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error: {e}")
            return {}

def process_transactions(wallet, tx_data):
    """
    Process transactions for a given wallet and return rows for CSV.
    Handles different data structures and converts values from Wei to ETH.
    """
    rows = []

    # If tx_data is a string, try parsing JSON
    if isinstance(tx_data, str):
        try:
            tx_data = json.loads(tx_data)
        except Exception as e:
            print(f"❌ Skipping wallet {wallet}: cannot parse string to JSON ({e})")
            return rows

    # Identify transaction list
    if isinstance(tx_data, dict):
        # Most common API response structure
        if 'items' in tx_data:
            transactions = tx_data['items']
        elif 'data' in tx_data and isinstance(tx_data['data'], dict) and 'items' in tx_data['data']:
            transactions = tx_data['data']['items']
        else:
            print(f"⚠ Wallet {wallet} has unexpected structure: {list(tx_data.keys())}")
            return rows
    elif isinstance(tx_data, list):
        transactions = tx_data
    else:
        print(f"⚠ Wallet {wallet} has unexpected structure: {type(tx_data)}")
        return rows

    # Process each transaction
    for tx in transactions:
        if not isinstance(tx, dict):
            continue

        # Decode method name if available
        decoded_name = tx.get('decoded', {}).get('name', '').lower()

        # Convert value (Wei to ETH if numeric)
        value_raw = tx.get('value', '')
        try:
            value_eth = float(value_raw) / 1e18 if value_raw else 0.0
        except (ValueError, TypeError):
            value_eth = 0.0

        rows.append({
            'wallet': wallet,
            'tx_hash': tx.get('tx_hash') or tx.get('hash', ''),
            'method': decoded_name,
            'value': round(value_eth, 6),  # Keep up to 6 decimal places
        })

    return rows

def save_processed_data(rows):
    """Save processed rows to CSV."""
    os.makedirs(os.path.dirname(PROCESSED_FILE), exist_ok=True)
    with open(PROCESSED_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['wallet', 'tx_hash', 'method', 'value'])
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Processed {len(rows)} transactions and saved to {PROCESSED_FILE}")

if __name__ == '__main__':
    raw_data = load_raw_data()
    if not raw_data:
        print("No raw data to process.")
        exit()

    all_rows = []
    # Show a sample structure for debugging
    first_wallet = next(iter(raw_data))
    print(f"🔍 First wallet: {first_wallet}, Type: {type(raw_data[first_wallet])}")
    sample_content = raw_data[first_wallet]
    print(f"Content sample keys: {list(sample_content.keys()) if isinstance(sample_content, dict) else 'N/A'}")

    # Process all wallets
    for wallet, tx_data in raw_data.items():
        wallet_rows = process_transactions(wallet, tx_data)
        all_rows.extend(wallet_rows)

    save_processed_data(all_rows)
