import os
import dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


dotenv.load_dotenv()

engine = create_engine(
   'mysql+mysqlconnector://nandnt3kz4k1kf99:l27kiziewok596ol@esilxl0nthgloe1y.chr7pe7iynqr.eu-west-1.rds.amazonaws.com:3306/zk6isj2zbdq8mq1h'
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