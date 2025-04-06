from pydantic import BaseModel, EmailStr

class UserSignup(BaseModel):
    app_name: str
    username: str
    email: EmailStr
    phone: str
    age: int
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str
