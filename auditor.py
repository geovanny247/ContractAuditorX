from fastapi import FastAPI, Request
from analyzer_module import analyze_contract
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.post("/audit")
async def audit_contract(request: Request):
    payload = await request.json()
    contract_code = payload.get("code")

    if not contract_code or not isinstance(contract_code, str):
        return {"error": "Código de contrato inválido o ausente"}

    report = analyze_contract(contract_code)
    return {"audit_report": report, "status": "success"}
