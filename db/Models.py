from sqlalchemy import Column, String, Integer, Text, DateTime, Date, Boolean, Float, ForeignKey, LargeBinary, Sequence, BLOB
from sqlalchemy.orm import relationship
from .database import Base, engine
from passlib.hash import bcrypt
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String(8))
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    avatar = Column(String(50))
    username = Column(String(20), unique=True)
    bio = Column(String(100))
    password = Column(String(128), nullable=False)
    state = Column(String(20))
    country = Column(String(20))
    email = Column(String(24), unique=True, nullable=False)
    phone = Column(String(24))
    registred_on = Column(Date)
    posts = relationship('Post', back_populates="user")
    
    
    @staticmethod
    def set_password_hash(pwd):
       return pwd_context.hash(pwd)
    
    @staticmethod
    def verify_password_hash(plain_pwd, hashed_pwd):
        return pwd_context.verify(plain_pwd, hashed_pwd)
    
    
    
class Post(Base):
    __tablename__ = "posts"
    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(100))
    description = Column(Text)
    url = Column(String(50), nullable=False)
    thumbnail = Column(String(50), nullable=False)
    created_at = Column(DateTime)
    size = Column(Float)
    likes = Column(Integer)
    views = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship('User', back_populates='posts')

    
    
    
Base.metadata.create_all(bind=engine)  