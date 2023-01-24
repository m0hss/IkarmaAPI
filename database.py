from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

USER_DATABASE_URL = "postgresql://m0:kwk5eEXleO3IW1IYMYMolVIcmqUjfVUo@dpg-cf7j40hmbjsp6ejgule0-a.frankfurt-postgres.render.com/ikarma_api"
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