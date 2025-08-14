from fastapi import FastAPI, Request, HTTPException
from webhook import pagos_confirmados

app = FastAPI()

@app.post("/audit")
async def audit(request: Request):
    try:
        data = await request.json()
        audit_id = data.get("audit_id")

        if not audit_id:
            raise HTTPException(status_code=400, detail="Falta el campo 'audit_id'")

        if audit_id not in pagos_confirmados:
            return {
                "status": "bloqueado",
                "mensaje": "🔒 Auditoría bloqueada. Realiza el pago para desbloquear.",
                "pago": f"https://commerce.coinbase.com/checkout/tu-checkout-id?audit_id={audit_id}"
            }

        # Simulación de auditoría real
        return {
            "status": "completado",
            "audit_id": audit_id,
            "issues_found": ["No hay validaciones explícitas en el contrato"],
            "total_issues": 1
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

