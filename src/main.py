from fastapi import FastAPI
from src.api import health

app = FastAPI()

app.include_router(health.router, prefix="/api")

@app.get("/")
async def health_check():
    return "Welcome! The server is running smoothly."
