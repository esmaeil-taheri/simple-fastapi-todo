from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True) 
    password = Column(String)
    first_name = Column(String)  
    last_name = Column(String)
    is_active = Column(Boolean)
    role = Column(String)
    phone_number = Column(String)   


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    user = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    