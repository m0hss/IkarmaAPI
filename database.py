from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

USER_DATABASE_URL = "mysql+mysqlconnector://root:qzDjhBdNJdVa0IHcSdJ9@containers-us-west-38.railway.app:6121/railway"

engine = create_engine(
    USER_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
# meta = MetaData()
# connexion = engine.connect()