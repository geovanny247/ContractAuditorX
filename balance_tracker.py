from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()
RPC_URL = os.getenv("RPC_URL")
MY_ADDRESS = os.getenv("MY_ADDRESS")

web3 = Web3(Web3.HTTPProvider(RPC_URL))

def get_balance():
    balance_wei = web3.eth.get_balance(MY_ADDRESS)
    return web3.fromWei(balance_wei, 'ether')

def check_profit(previous_balance):
    current_balance = get_balance()
    difference = current_balance - previous_balance

    if difference > 0:
        print(f"💰 ¡Ganancia detectada! +{difference:.6f} MATIC")
    elif difference == 0:
        print("🟡 No hubo cambio en el saldo.")
    else:
        print(f"🔻 El saldo bajó: -{abs(difference):.6f} MATIC")

    return current_balance
