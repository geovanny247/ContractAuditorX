from fastapi import FastAPI, Request
import requests

app = FastAPI()

NODE_URL = "https://polygon-mainnet.g.alchemy.com/v2/YOUR_ALCHEMY_KEY"

@app.post("/rpc")
async def proxy_rpc(request: Request):
    body = await request.json()
    method = body.get("method")
    params = body.get("params")

    # Interceptar solo métodos sensibles
    if method in ["eth_sendTransaction", "eth_estimateGas"]:
        contract_address = params[0].get("to")

        # Auditar contrato
        audit_response = requests.post("https://contractauditorx.onrender.com/audit", json={"code": contract_address})
        audit_result = audit_response.json()

        if audit_result.get("status") != "pendiente":
            return {"error": "Auditoría fallida o no generada"}

        charge_id = audit_result.get("charge_id")

        # Verificar pago
        verify_response = requests.post("https://contractauditorx.onrender.com/verify-payment", json={
            "charge_id": charge_id,
            "code": contract_address
        })

        verify_result = verify_response.json()
        if verify_result.get("status") != "paid":
            return {"error": "Pago requerido para continuar"}

    # Si todo está bien, reenviar al nodo real
    response = requests.post(NODE_URL, json=body)
    return response.json()
