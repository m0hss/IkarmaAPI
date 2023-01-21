from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List, Literal
from passlib.context import CryptContext




class Post(BaseModel):
    id: Optional[int]
    pass