# filepath: d:\KARAM\project\auth-microservice\app\main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from app.routes import router
from app.logger import logger
from fastapi.responses import JSONResponse
import os

# Determine environment
ENV = os.getenv("ENV","dev")  # Default to 'development'
print(f"Environment: {ENV}")
# Middlewares
middleware = [
    Middleware(TrustedHostMiddleware, allowed_hosts=[
        "auth-microservice.onrender.com", "*.onrender.com", "localhost", "127.0.0.1"
    ]),
    Middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
]

if ENV == "prod":
    middleware.append(Middleware(HTTPSRedirectMiddleware))
else:
    middleware = []
    logger.warning("⚠️ Running in development mode. HTTPS redirect is disabled.")
# FastAPI app
app = FastAPI(
    title="Universal Authentication Service 🚀",
    version="1.0",
    middleware=middleware  if middleware else None 
)

APP_URL = os.getenv("APP_URL", "http://localhost:8000")  # fallback for local

# ➡️ Add this basic health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/", tags=["Root"])
async def root():
    logger.info("App Root Endpoint Accessed")
    return JSONResponse(content={
        "message": "🚀 Authentication Microservice is Running!",
        "app_url": APP_URL
    })

# Include router
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Authentication Service Started!")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 Authentication Service Stopped!")