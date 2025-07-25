import csv
import os

PROCESSED_FILE = 'data/processed_data.csv'
RISK_SCORES_FILE = 'data/risk_scores.csv'
RISK_DETAILS_FILE = 'data/risk_score_details.csv'


def load_processed_data():
    """Load processed transactions from CSV."""
    if not os.path.exists(PROCESSED_FILE):
        print(f"❌ Processed data file {PROCESSED_FILE} not found.")
        return []

    with open(PROCESSED_FILE, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)


def calculate_raw_scores(transactions):
    """
    Calculate raw risk score components for each wallet.
    Features:
        - +2 points per transaction
        - +10 points for high-value transfers (> 1 ETH)
        - +5 points for suspicious methods (unknown/fallback)
        - +0.5 * ETH value
    """
    raw_scores = {}
    details = []  # detailed breakdown

    for tx in transactions:
        wallet = tx['wallet']
        method = tx['method']
        value_raw = tx['value']

        try:
            value = float(value_raw) if value_raw else 0.0
        except ValueError:
            value = 0.0

        if wallet not in raw_scores:
            raw_scores[wallet] = 0

        # Base +2 points per transaction
        raw_scores[wallet] += 2
        details.append([wallet, tx['tx_hash'], "+2", "Transaction recorded"])

        # High-value transfer
        if value > 1.0:
            raw_scores[wallet] += 10
            details.append([wallet, tx['tx_hash'], "+10", f"High-value transfer ({value} ETH)"])

        # Suspicious method
        if method in ('', 'unknown', 'fallback'):
            raw_scores[wallet] += 5
            details.append([wallet, tx['tx_hash'], "+5", f"Suspicious or unknown method '{method}'"])

        # Add value-based score
        if value > 0:
            points = 0.5 * value
            raw_scores[wallet] += points
            details.append([wallet, tx['tx_hash'], f"+{points:.2f}", f"Value contribution ({value} ETH)"])

    return raw_scores, details


def normalize_scores(raw_scores):
    """Normalize scores to 0–1000."""
    if not raw_scores:
        return {}

    max_score = max(raw_scores.values())
    if max_score == 0:
        return {wallet: 0 for wallet in raw_scores}

    normalized = {
        wallet: round((score / max_score) * 1000, 2)
        for wallet, score in raw_scores.items()
    }
    return normalized


def save_risk_scores(scores):
    """Save normalized risk scores to CSV."""
    os.makedirs(os.path.dirname(RISK_SCORES_FILE), exist_ok=True)
    with open(RISK_SCORES_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['wallet', 'risk_score'])
        for wallet, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
            writer.writerow([wallet, score])
    print(f"✅ Risk scores saved to {RISK_SCORES_FILE}")


def save_risk_details(details):
    """Save detailed scoring breakdown to CSV."""
    os.makedirs(os.path.dirname(RISK_DETAILS_FILE), exist_ok=True)
    with open(RISK_DETAILS_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['wallet', 'tx_hash', 'points', 'reason'])
        writer.writerows(details)
    print(f"📜 Detailed scoring breakdown saved to {RISK_DETAILS_FILE}")


if __name__ == '__main__':
    transactions = load_processed_data()
    if not transactions:
        print("No transactions to score.")
        exit()

    raw_scores, details = calculate_raw_scores(transactions)
    normalized_scores = normalize_scores(raw_scores)
    save_risk_scores(normalized_scores)
    save_risk_details(details)

    print("\n📢 Risk scoring completed based on:")
    print("   • +2 points per transaction")
    print("   • +10 points for transfers > 1 ETH")
    print("   • +5 points for suspicious methods")
    print("   • +0.5 * ETH value contribution")
    print("   • Normalized to 0–1000 using max raw score.")
