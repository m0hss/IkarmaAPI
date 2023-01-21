from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text, Date, Boolean
from database import Base, engine
from passlib.hash import bcrypt
from passlib.context import CryptContext



class Post(Base):
    __tablename__ = "posts"
    pass