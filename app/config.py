from supabase import create_client, Client
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Environment variables for Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_API_KEY = os.getenv("SUPABASE_API_KEY")

if not SUPABASE_URL or not SUPABASE_API_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_API_KEY must be set in environment variables.")

# Initialize Supabase client
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)