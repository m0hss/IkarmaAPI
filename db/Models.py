from sqlalchemy import Column, String, Integer, Text, DateTime, Date, Boolean, Float, ForeignKey, LargeBinary, Sequence
from sqlalchemy.orm import relationship
from .database import Base, engine
from passlib.hash import bcrypt
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String(8))
    first_name = Column(String(20))
    last_name = Column(String(20))
    thumbnail = Column(String(100))
    username = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    city = Column(String(20))
    state = Column(String(20))
    country = Column(String(20))
    email = Column(String(64))
    phone = Column(String(24))
    registred_on = Column(Date)
    is_active = Column(Boolean)
    posts = relationship('PostModel.Post', back_populates="user")
    
    
    @staticmethod
    def get_password_hash(password):
       return pwd_context.hash(password)
    
    @staticmethod
    def verify_password_hash(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)
    
    
    
class Post(Base):
    __tablename__ = "posts"
    id = Column(String(36), primary_key=True, index=True)
    title = Column(String(100))
    description = Column(Text)
    path = Column(String(50), nullable=False)
    created_at = Column(DateTime)
    size = Column(Float)
    likes = Column(Integer)
    views = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship('UserModel.User', back_populates='posts')
    
    
    
Base.metadata.create_all(bind=engine)  