from fastapi import FastAPI
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
ALCHEMY_API_KEY = os.getenv("ALCHEMY_API_KEY")

@app.get("/")
async def root():
    return {"message": "Alchemy listener activo"}

@app.get("/check")
async def check_alchemy():
    url = f"https://polygon-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return {"status_code": response.status_code}
