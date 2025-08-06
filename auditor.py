from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from analyzer_module import analyze_contract
from dotenv import load_dotenv
import os

# 🔐 Cargar variables de entorno
load_dotenv()
app = FastAPI()

# 🌐 Middleware CORS blindado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],           # permite todos los métodos
    allow_headers=["*"],           # permite todos los headers
)

# ✅ Modelo de entrada
class ContractRequest(BaseModel):
    code: str

# 🔍 Endpoint principal
@app.post("/audit")
async def audit_contract(payload: ContractRequest):
    try:
        report = analyze_contract(payload.code)
        return JSONResponse(
            status_code=200,
            content={
                "audit_report": report,
                "status": "success",
                "payment_url": os.getenv("COINBASE_CHECKOUT_URL")
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Error interno: {str(e)}"}
        )

# 🛡️ Endpoint manual para OPTIONS /audit (preflight CORS)
@app.options("/audit")
async def options_audit(request: Request):
    return JSONResponse(
        status_code=200,
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )

# 🛡️ Endpoint manual para OPTIONS /
@app.options("/")
async def options_root():
    return JSONResponse(
        status_code=200,
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "*"
        }
    )



