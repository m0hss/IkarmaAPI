from fastapi import UploadFile
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional, List, Literal
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .post_schema import Post


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    id: Optional[int]
    gender: Optional[Literal['male', 'female']] = None
    first_name: str 
    last_name: str
    avatar: str = None
    username: str = None
    bio: str = None
    password: str
    state: str = None
    country: str = None
    email: str 
    phone: int = None
    registred_on: date = None
    posts: Optional[List[Post]] = []
    
    @staticmethod
    def set_password_hash(pwd):
        return pwd_context.hash(pwd)

    class Config:
        orm_mode= True
        
    
        

class Useradd(BaseModel):
    first_name: str = Field(min_length=3, max_length=20)
    last_name: str
    email: str
    password: str
    
    
    @staticmethod
    def set_password_hash(pwd):
        return pwd_context.hash(pwd)

    class Config:
        orm_mode= True


class UserUpdate(BaseModel):
    gender: Optional[Literal['male', 'female']] = None
    first_name: Optional[str]
    last_name: Optional[str] 
    # thumbnail: Optional[str] = None
    username: Optional[str] = None
    bio: Optional[str] = None
    password: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[int] = None
    # registred_on: Optional[date] = None

    class Config:
        orm_mode= True


class ReadPosts(Post):
    id: Optional[str]
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    # data: Optional[bytes] = None
    views: Optional[int] = None
    likes: Optional[int] = None
    created_at: Optional[datetime] = None
    size: Optional[int] = None
    user_id : Optional[int] = None
    user: User
    
    class Config:
        orm_mode= True


class reponse(BaseModel):
    msg: str

# class Token(BaseModel):
#     access_token: str
#     token_type: str