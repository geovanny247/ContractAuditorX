from fastapi import APIRouter

router = APIRouter()

@router.get("/check-payment")
async def check_payment():
    # Simulación de pago validado
    return {"paid": True}
