from fastapi import APIRouter

router = APIRouter()

@router.get("/report")
async def get_report():
    # Simulación de informe
    return {
        "summary": "Contrato auditado correctamente",
        "score": 92,
        "recommendations": ["Evita funciones sin visibilidad", "Usa SafeMath"]
    }
