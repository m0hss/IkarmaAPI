from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List, Literal
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    id: Optional[int]
    gender: Literal['male', 'female']
    first_name: str = Field(min_length=3, max_length=20)
    last_name: str
    thumbnail: str
    username: str 
    password_hash: str
    city: str
    state: str
    country: str
    email: str
    phone: int
    registred_on: date = None
    is_active: Optional[bool] = False
    
    @staticmethod
    def set_password_hash(password):
        return pwd_context.hash(password)
    
    class Config:
        orm_mode= True
        

class UserUpdate(User):
    gender: Optional[Literal['male', 'female']] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    thumbnail: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[int] = None
    registred_on: Optional[date] = None
    is_active: Optional[bool] = False

    class Config:
        orm_mode= True


class reponse(BaseModel):
    msg: str

class Token(BaseModel):
    access_token: str
    token_type: str