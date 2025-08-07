from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from analyzer_module import analyze_contract
from dotenv import load_dotenv
import os
import httpx

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContractRequest(BaseModel):
    code: str

@app.post("/audit")
async def audit_contract(payload: ContractRequest):
    try:
        report = analyze_contract(payload.code)

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.commerce.coinbase.com/checkouts",
                headers={
                    "X-CC-Api-Key": os.getenv("COINBASE_API_KEY"),
                    "Content-Type": "application/json"
                },
                json={
                    "name": "Auditoría de contrato",
                    "pricing_type": "fixed_price",
                    "local_price": {
                        "amount": "5.00",
                        "currency": "USDC"
                    }
                }
            )

        checkout = response.json()
        payment_url = checkout.get("hosted_url")

        return JSONResponse(
            status_code=200,
            content={
                "audit_report": report,
                "status": "success",
                "payment_url": payment_url
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error interno: {str(e)}"}
        )

@app.post("/verify-payment")
async def verify_payment(request: Request):
    try:
        data = await request.json()
        charge_id = data.get("charge_id")
        code = data.get("code")

        if not charge_id or not code:
            return JSONResponse(
                status_code=400,
                content={"error": "Faltan parámetros: charge_id y code"}
            )

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.commerce.coinbase.com/charges/{charge_id}",
                headers={
                    "X-CC-Api-Key": os.getenv("COINBASE_API_KEY")
                }
            )

        charge = response.json()
        status = charge.get("timeline", [{}])[-1].get("status")

        if status == "COMPLETED":
            report = analyze_contract(code)
            return JSONResponse(
                status_code=200,
                content={
                    "audit_report": report,
                    "status": "paid"
                }
            )
        else:
            return JSONResponse(
                status_code=402,
                content={"error": "Pago no completado", "status": status}
            )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error interno: {str(e)}"}
        )




