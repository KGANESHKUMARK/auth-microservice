from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from app.routes import router
from app.logger import logger

# Middlewares
middleware = [
    Middleware(TrustedHostMiddleware, allowed_hosts=[
        "auth-microservice.onrender.com", "*.onrender.com", "localhost", "127.0.0.1"
    ]),
    Middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]),
    Middleware(HTTPSRedirectMiddleware)
]

# FastAPI app
app = FastAPI(
    title="Universal Authentication Service 🚀",
    version="1.0",
    middleware=middleware
)

# Include router
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Authentication Service Started!")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 Authentication Service Stopped.")
