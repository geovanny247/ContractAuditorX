from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/check")
async def check():
    return {"status": "ok"}

@app.post("/audit")
async def audit(request: Request):
    data = await request.json()
    print("Contrato recibido:", data)
    return {"message": "Contrato auditado"}
