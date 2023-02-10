from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, Field 
from typing import Optional, List, Literal
from datetime import datetime
import json
from Schemas import UserSchema

class Post(BaseModel):
    id: str
    title: str
    description: str
    path: str
    created_at: datetime
    size: float
    views: Optional[int] = None
    likes: Optional[int] = None
    user_id: int
    # user: Optional[List[UserSchema.User]] = []
    class Config:
        orm_mode= True


class ReadPost(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    data: Optional[bytes] = None
    views: Optional[int] = None
    likes: Optional[int] = None
    created_at: Optional[datetime] = None
    user_id : int
    
    class Config:
        orm_mode= True
        
class reponse(BaseModel):
    msg: str