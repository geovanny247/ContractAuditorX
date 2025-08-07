import requests
import time

ALCHEMY_URL = "https://polygon-mainnet.g.alchemy.com/v2/YOUR_API_KEY"
AUDIT_URL = "https://contractauditorx.onrender.com/audit"
CONTRACTS = ["0x123...", "0x456..."]  # Añade direcciones que quieras monitorear

def listen():
    while True:
        for contract in CONTRACTS:
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "alchemy_getAssetTransfers",
                "params": [{
                    "fromBlock": "latest",
                    "toAddress": contract,
                    "category": ["external", "contract"],
                    "withMetadata": True
                }]
            }
            res = requests.post(ALCHEMY_URL, json=payload)
            data = res.json()
            if data.get("result", {}).get("transfers"):
                requests.post(AUDIT_URL, json={"contract": contract})
        time.sleep(60)
