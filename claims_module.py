from web3 import Web3
import os
from dotenv import load_dotenv
from balance_tracker import get_balance, check_profit  # 👈 módulo que monitorea ganancias

# 🧪 Cargar variables de entorno
load_dotenv()

# 🔐 Variables sensibles
RPC_URL = os.getenv("RPC_URL")
MY_ADDRESS = os.getenv("MY_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# 🛠️ Inicializar Web3
web3 = Web3(Web3.HTTPProvider(RPC_URL))

# 🔍 Verificar conexión
if not web3.isConnected():
    raise ConnectionError("No se pudo conectar con el nodo RPC.")

# 🚀 Ejecutar retiro del contrato y monitorear ganancias
def claimFunds(contract_address, abi):
    try:
        contract = web3.eth.contract(address=contract_address, abi=abi)

        # 🧮 Saldo antes de ejecutar
        previous_balance = get_balance()

        tx = contract.functions.withdraw().buildTransaction({
            'from': MY_ADDRESS,
            'nonce': web3.eth.getTransactionCount(MY_ADDRESS, 'pending'),
            'gas': 200000,
            'gasPrice': web3.toWei('50', 'gwei')
        })

        signed_tx = web3.eth.account.signTransaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(f"Transacción enviada: {web3.toHex(tx_hash)}")

        # 🧾 Esperar confirmación
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            print("✅ Transacción confirmada.")
        else:
            print("❌ La transacción fue rechazada en el contrato.")

        # 📊 Verificar ganancia
        check_profit(previous_balance)

        return web3.toHex(tx_hash)

    except Exception as e:
        print(f"Error al ejecutar claim: {str(e)}")
        return None

