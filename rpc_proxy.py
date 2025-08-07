from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import requests
import os

app = FastAPI()

# URL del nodo real (Alchemy)
NODE_URL = "https://polygon-mainnet.g.alchemy.com/v2/" + os.getenv("ALCHEMY_KEY")

@app.post("/rpc")
async def proxy_rpc(request: Request):
    body = await request.json()
    method = body.get("method")
    params = body.get("params")

    # Interceptar solo métodos sensibles
    if method in ["eth_sendTransaction", "eth_estimateGas"]:
        try:
            contract_address = params[0].get("to")

            # Paso 1: Generar auditoría y pago
            audit_response = requests.post(
                "https://contractauditorx.onrender.com/audit",
                json={"code": contract_address}
            )
            audit_result = audit_response.json()

            if audit_result.get("status") != "pendiente":
                return JSONResponse(
                    status_code=400,
                    content={"error": "Auditoría fallida o no generada"}
                )

            charge_id = audit_result.get("charge_id")

            # Paso 2: Verificar pago
            verify_response = requests.post(
                "https://contractauditorx.onrender.com/verify-payment",
                json={
                    "charge_id": charge_id,
                    "code": contract_address
                }
            )
            verify_result = verify_response.json()

            if verify_result.get("status") != "paid":
                return JSONResponse(
                    status_code=402,
                    content={
                        "error": "Pago requerido para continuar",
                        "status": verify_result.get("status")
                    }
                )

        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"error": f"Error interno en proxy: {str(e)}"}
            )

    # Si todo está bien, reenviar al nodo real
    try:
        response = requests.post(NODE_URL, json=body)
        return JSONResponse(status_code=response.status_code, content=response.json())
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error al reenviar al nodo: {str(e)}"}
        )

