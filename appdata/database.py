# database.py
from CBI import debug
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///users.db"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def start_session():
    from sqlalchemy.orm import sessionmaker
    session = sessionmaker(bind=engine)()
    session.begin()
    return session

def Print(*args, documentation=False):
    if debug[0]:
        print(" ".join(args))
