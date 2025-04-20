from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

import os

load_dotenv()

# Sqlite
# SQLACLHEMY_DATABASE_URL = 'sqlite:///./app.db'
# engine = create_engine(SQLACLHEMY_DATABASE_URL, connect_args={'check_same_thread': False}, echo=True)


SQLACLHEMY_DATABASE_URL =  os.environ.get("DATABASE_URL")


engine = create_engine(SQLACLHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()
