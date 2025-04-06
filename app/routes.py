from fastapi import APIRouter, HTTPException
from app.models import UserSignup, UserLogin
from app.config import supabase_client
from app.logger import logger

router = APIRouter()

@router.post("/signup")
async def signup(user: UserSignup):
    try:
        response = supabase_client.auth.sign_up(
            {
                "email": user.email,
                "password": user.password,
                "options": {
                    "data": {
                        "username": user.username,
                        "phone": user.phone,
                        "age": user.age,
                        "app_name": user.app_name
                    }
                }
            }
        )
        logger.info(f"User signed up: {user.email} from {user.app_name}")
        return {"message": "User signed up successfully. Please verify your email."}
    except Exception as e:
        logger.error(f"Signup failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user: UserLogin):
    try:
        response = supabase_client.auth.sign_in_with_password(
            {"email": user.email, "password": user.password}
        )
        logger.info(f"User login: {user.email}")
        return {"message": "User logged in successfully.", "session": response}
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
