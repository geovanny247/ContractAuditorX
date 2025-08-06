from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from analyzer_module import analyze_contract
from dotenv import load_dotenv
import os

# 🔐 Cargar variables de entorno
load_dotenv()

# 🚀 Instancia de FastAPI
app = FastAPI()

# 🌐 Middleware CORS blindado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # o reemplazá con tu dominio frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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




