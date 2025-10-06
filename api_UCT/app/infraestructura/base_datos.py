from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import DB_URL

connect_args = {'check_same_thread': False} if DB_URL.startswith('sqlite') else {}
engine = create_engine(DB_URL, connect_args=connect_args)
SesionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def obtener_db():
    db = SesionLocal()
    try:
        yield db
    finally:
        db.close()
