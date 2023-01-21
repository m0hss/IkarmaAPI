from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

USER_DATABASE_URL = "mysql+mysqlconnector://b7890773c1228a:181896d6@eu-cdbr-west-03.cleardb.net/heroku_fb822d9648d206b"
# USER_DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/ikarma"

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