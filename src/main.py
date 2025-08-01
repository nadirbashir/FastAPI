from fastapi import FastAPI
from contextlib import asynccontextmanager
from .health import router as health_router
from .auth.controller import router as auth_router
from .user.controller import router as user_router
from .database.core import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    
    init_db()
    print("✅ Database initialized")

    yield
    print("🔴 Shutting down the application")


app = FastAPI(lifespan=lifespan)

app.include_router(health_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(user_router, prefix="/api")

@app.get("/")
async def health_check():
    return "Welcome! The server is running smoothly."

