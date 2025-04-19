from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


# SQLACLHEMY_DATABASE_URL =  'postgresql://postgres:esi12345@localhost:5432/store'

SQLACLHEMY_DATABASE_URL = 'sqlite:///./app.db'


engine = create_engine(SQLACLHEMY_DATABASE_URL, connect_args={'check_same_thread': False}, echo=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


# insert into todos (title, description, priority, complete) values ('go home', 'sleep', 1, False)

# .mode table
