from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI()

# Modelo de entrada
class AuditRequest(BaseModel):
    audit_id: str
    code: str

# Simulación de base de datos de pagos
pagos = {}

@app.post("/audit")
def audit_contract(data: AuditRequest):
    try:
        # Simulación: si no se ha pagado, generar checkout
        if data.audit_id not in pagos:
            checkout_id = str(uuid.uuid4())
            pagos[data.audit_id] = {
                "status": "bloqueado",
                "checkout_id": checkout_id
            }
            return {
                "status": "bloqueado",
                "mensaje": "🔒 Auditoría bloqueada. Realiza el pago para desbloquear.",
                "pago": f"https://commerce.coinbase.com/checkout/{checkout_id}?audit_id={data.audit_id}"
            }

        # Si ya se pagó
        return {
            "status": "desbloqueado",
            "mensaje": "✅ Auditoría desbloqueada.",
            "resultado": "El contrato es seguro (simulado)"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


