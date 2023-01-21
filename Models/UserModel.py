from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text, Date, Boolean
from database import Base, engine
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
    
    
    def active(self):
        self.is_active = True
    
    @staticmethod
    def get_password_hash(password):
       return pwd_context.hash(password)
    
    @staticmethod
    def verify_password_hash(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

Base.metadata.create_all(bind=engine)  