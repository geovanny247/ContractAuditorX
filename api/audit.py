from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()

class AuditRequest(BaseModel):
    bytecode: str

@router.post("/audit")
async def audit_contract(data: AuditRequest):
    # Simulación de auditoría
    if "unsafe" in data.bytecode:
        return {"passed": False, "issues": ["Unsafe opcode detected"]}
    return {"passed": True, "issues": []}
