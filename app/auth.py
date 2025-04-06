import os
from dotenv import load_dotenv
from fastapi import HTTPException
import logging
from supabase import create_client

# Load environment variables
load_dotenv()

# Setup logging
logger = logging.getLogger(__name__)

# Connect to Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")
supabase_client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def signup_user(user):
    try:
        response = supabase_client.auth.sign_up(
            {
                "email": user.email,
                "password": user.password,
                "options": {
                    "data": {
                        "username": user.username,
                        "phone": user.phone,
                        "age": user.age
                    }
                }
            }
        )
        logger.info(f"✅ User signup successful: {user.email}")
        return {"message": "User signed up successfully. Please verify your email."}
    except Exception as e:
        logger.error(f"❌ Signup failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

def login_user(user):
    try:
        response = supabase_client.auth.sign_in_with_password(
            {
                "email": user.email,
                "password": user.password
            }
        )
        logger.info(f"✅ User login successful: {user.email}")
        return {"message": "Login successful", "session": response.session}
    except Exception as e:
        logger.error(f"❌ Login failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))

def get_user_details(token: str):
    """
    Fetch user details using the provided authentication token.
    """
    try:
        user = supabase_client.auth.get_user(token)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        logger.info(f"✅ Fetched user details for token: {token}")
        return {"message": "User details fetched successfully.", "user": user}
    except Exception as e:
        logger.error(f"❌ Failed to fetch user details: {e}")
        raise HTTPException(status_code=400, detail=str(e))

def get_all_users():
    """
    Fetch all user details.
    """
    try:
        response = supabase_client.auth.admin.list_users()
        users = response.get("users", [])
        logger.info(f"✅ Fetched {len(users)} users.")
        return {"message": "All users fetched successfully.", "users": users}
    except Exception as e:
        logger.error(f"❌ Failed to fetch all users: {e}")
        raise HTTPException(status_code=400, detail=str(e))