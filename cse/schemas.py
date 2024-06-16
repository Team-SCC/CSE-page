from pydantic import BaseModel
from datetime import date

class UserCreate(BaseModel):
    id: int
    password: str
    name: str
    auth: int
    email: str

class UserUpdate(BaseModel):
    name: str
    gender: str
    grade: int
    phone: str
    birth: date
    password: str
    nickname: str
    email: str
    
class UserLogin(BaseModel):
    id: int
    password: str

class SessionData(BaseModel):
    username: str