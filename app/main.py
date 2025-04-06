from fastapi import FastAPI, HTTPException
from starlette.middleware import Middleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.models import UserSignup, UserLogin
from app.auth import signup_user, login_user
import logging

# Setup middlewares
middleware = [
    Middleware(TrustedHostMiddleware, allowed_hosts=[
        "snapscore.onrender.com", "*.onrender.com", "localhost", "127.0.0.1"
    ]),
    Middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"]),
    Middleware(HTTPSRedirectMiddleware)
]

app = FastAPI(
    title="SnapScore Authentication Microservice 🚀",
    version="1.0",
    middleware=middleware
)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 SnapScore Authentication Microservice Started!")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("👋 SnapScore Authentication Microservice Stopped.")

# Sign Up Endpoint
@app.post("/signup")
async def signup(user: UserSignup):
    return signup_user(user)

# Login Endpoint
@app.post("/login")
async def login(user: UserLogin):
    return login_user(user)
