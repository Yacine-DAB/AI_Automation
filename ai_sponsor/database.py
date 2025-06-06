from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SLQALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'

engine = create_engine(
     SLQALCHEMY_DATABASE_URL,
     connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

def get_db():
     db = SessionLocal()
     try:
          yield db
     finally:
          db.close()
          
          