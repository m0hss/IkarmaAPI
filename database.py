from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


USER_DATABASE_URL = "postgresql://m0:vMqDPtG4avjyxRzX7vOpIlfan8QqMfBF@dpg-cf7ch9mn6mplrj35m8u0-a.frankfurt-postgres.render.com/ikarma_api_pgsql"
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