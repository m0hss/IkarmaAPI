from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Dict
from datetime import datetime
import json
# from .user_schema import User


class Post(BaseModel):
    id: str
    title: str
    description: str
    url: str
    thumbnail: Optional[str] = None
    created_at: datetime
    size: float
    views: Optional[int] = None
    likes: Optional[int] = None
    user_id: int
    #user: User
    
    # def to_dict(self):
    #     data = self.dict()
    #     user = User.get(id=self.user_id)
    #     data['user'] = user.username
    #     return data
    
    class Config:
        orm_mode= True


class ReadPost(Post):
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
    # user: User
    
    class Config:
        orm_mode= True
           


class PostUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

        
class reponse(BaseModel):
    msg: str