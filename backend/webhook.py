from fastapi import FastAPI, Request
import json

app = FastAPI()

# Simulación de base de datos en memoria
pagos_confirmados = {}

@app.post("/coinbase-webhook")
async def coinbase_webhook(request: Request):
    payload = await request.json()
    event_type = payload.get("event", {}).get("type")

    if event_type == "charge:confirmed":
        metadata = payload["event"]["data"]["metadata"]
        audit_id = metadata.get("audit_id")
        wallet = metadata.get("wallet_address")

        pagos_confirmados[audit_id] = wallet
        print(f"✅ Pago confirmado para audit_id: {audit_id}, wallet: {wallet}")

    return {"status": "ok"}

