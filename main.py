from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import User, Base
from database import engine, SessionLocal
from utils import hash_password, verify_password
import uvicorn
from pydantic import BaseModel, EmailStr
import os

app = FastAPI(title="Auth Microservice 🔥")

# Create tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Dependency
async def get_db():
    async with SessionLocal() as session:
        yield session

# Schemas
class UserCreate(BaseModel):
    username: str
    phone_number: str
    email: EmailStr
    password: str
    age: int

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Routes
@app.post("/signup")
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    result = await db.execute(select(User).where((User.email == user.email) | (User.username == user.username)))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or Email already registered.")

    new_user = User(
        username=user.username,
        phone_number=user.phone_number,
        email=user.email,
        hashed_password=hash_password(user.password),
        age=user.age,
    )
    db.add(new_user)
    await db.commit()
    return {"message": "User created successfully"}

@app.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalars().first()

    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid Credentials.")

    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Credentials.")

    return {"message": f"Welcome back, {existing_user.username}!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
