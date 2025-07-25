# 🔐 Zeru – Wallet Risk Scoring From Scratch

## 📌 Problem Statement

The goal is to evaluate the risk profile of a set of wallet addresses interacting with lending protocols (Aave V2, Compound V2/V3) by analyzing their on-chain transaction history. This involves retrieving raw blockchain data, extracting meaningful features (e.g., transaction frequency, borrow/repay patterns, and asset movements), and developing a risk scoring model that assigns each wallet a score between 0 and 1000. 

The final output is a structured CSV containing each wallet's ID and corresponding risk score, with clear documentation of feature selection, normalization, and scoring logic.

The higher the score, the riskier the wallet may be.

---

## 🧠 Method Chosen

#### Data Collection 

Collected transaction history of wallets from blockchain data providers like Covalent. This raw data is saved in a file called data/raw_transactions.json.

The script process_data.py reads this data and extracts important details such as:

The wallet address.
How many transactions it made.
The value (amount of ETH) in those transactions.
What type of activity (e.g., interacting with smart contracts).

This cleaned data is then saved in a simpler file called data/processed_data.csv.

### Feature Selection Rationale
To judge if a wallet might be risky, we look at:

Number of Transactions – If a wallet is sending/receiving a lot of transactions, it might be used by bots or hackers.

Total ETH Volume – Very high-value transfers might indicate scams or suspicious activity.

Smart Contract Activity – If a wallet interacts with too many smart contracts, it could be exposed to bugs or hacks in those contracts.

Frequency – If transactions happen too often in a short time, that can be suspicious.

### How We Calculate the Risk Score
We give each feature (transaction count, total volume, etc.) a score between 0 and 1 (0 = low, 1 = high).

Then we combine these scores using weights (some features matter more than others).

30% from transaction count.
30% from total ETH transferred.
20% from contract activity.
20% from frequency of transactions.

Finally, the total score is multiplied by 1000 to give a final risk score between 0 and 1000.

### Justification of Risk Indicators
Transaction count and volume – Scam wallets often have very high or very low activity compared to normal wallets.

Contract calls – Interacting with many unknown tokens or contracts is risky because of possible fraud.

Frequency of transactions – Bots or hacked wallets usually make transactions in bursts.

This method is simple, easy to update, and works well for large sets of wallets.

### How to Use It
Save your blockchain transaction data in data/raw_transactions.json.

Run the command:

python process_data.py
This will create a clean file data/processed_data.csv.

Then run:

python risk_scoring.py
This will create:

data/wallet_risk_scores.csv – Final risk scores for each wallet.

data/risk_scoring_explanation.csv – A breakdown of why each wallet got its score.

### Why It’s Scalable
This approach can work for thousands of wallets with no issue.



### 🧮 Scoring Formula (Simplified)


Risk Score=(Weighted Features)×1000

We assign a risk score between 0 and 1000 using a weighted formula based on key risk indicators:


Risk Score=1000×(0.4⋅Rbs+0.3⋅R liq+0.2⋅Rfreq +0.1⋅Rnet)

Where:

𝑅𝑏𝑠= Normalized Borrow-to-Supply Ratio

𝑅𝑙𝑖𝑞= Liquidation Risk (1 if liquidation detected, else 0)

𝑅𝑓𝑟𝑒𝑞 = Normalized Transaction Frequency 

𝑅𝑛𝑒𝑡 = Normalized Net Position Risk (borrowed minus supplied assets)​



## 🚀 How to Run

bash
```
pip install -r requirements.txt

python fetch_transactions.py
python process_data.py 
python risk_scoring.py

```
