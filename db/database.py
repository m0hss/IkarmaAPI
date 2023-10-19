import os
import dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


dotenv.load_dotenv()
engine = create_engine(
    os.getenv('USER_DATABASE_URL')
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
# Base.metadata.create_all(bind=engine)