from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./hotel_reservations.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})#Concurrent Tool Execution

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)#CRUD
Base = declarative_base()#Creating database tables

def get_db():
    '''Provides a context-generator helper function that yields a database session
      and ensures it is safely closed after use.'''
    db = session_local()
    try:
        yield db
    finally:
        db.close()