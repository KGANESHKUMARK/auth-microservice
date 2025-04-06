from fastapi import APIRouter, HTTPException, Depends
from app.models import UserSignup, UserLogin
from app.config import supabase_client
from app.logger import logger
import bcrypt

router = APIRouter()


@router.post("/signup")
async def signup(user: UserSignup):
    try:
        # Hash the password
        hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Sign up to Auth
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
        
        # Insert into your database table
        user_data = {
            "email": user.email,
            "username": user.username,
            "phone": user.phone,
            "password": hashed_password,  # Store the hashed password
            "age": user.age,
            "app_name": user.app_name
        }
        
        supabase_client.table("users").insert(user_data).execute()

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

@router.get("/user")
async def get_user_details(token: str):
    """
    Fetch user details using the provided authentication token.
    """
    try:
        user = supabase_client.auth.get_user(token)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        logger.info(f"Fetched user details for token: {token}")
        return {"message": "User details fetched successfully.", "user": user}
    except Exception as e:
        logger.error(f"Failed to fetch user details: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/users")
async def get_all_users():
    """
    Fetch all user details.
    """
    try:
        response = supabase_client.auth.admin.list_users()
        users = response.get("users", [])
        logger.info(f"Fetched {len(users)} users.")
        return {"message": "All users fetched successfully.", "users": users}
    except Exception as e:
        logger.error(f"Failed to fetch all users: {e}")
        raise HTTPException(status_code=400, detail=str(e))