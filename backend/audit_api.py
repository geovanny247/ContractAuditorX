from fastapi import FastAPI, Request
from webhook import pagos_confirmados

app = FastAPI()

@app.post("/audit")
async def audit(request: Request):
    data = await request.json()
    audit_id = data.get("audit_id")

    if audit_id not in pagos_confirmados:
        return {
            "status": "bloqueado",
            "mensaje": "🔒 Auditoría bloqueada. Realiza el pago para desbloquear.",
            "pago": f"https://commerce.coinbase.com/checkout/tu-checkout-id?audit_id={audit_id}"
        }

    # Aquí va tu lógica de auditoría real
    return {
        "issues_found": ["No hay validaciones explícitas en el contrato"],
        "total_issues": 1
    }
