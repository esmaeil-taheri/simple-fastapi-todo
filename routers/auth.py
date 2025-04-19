from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from starlette import status
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone
import os

from models import Users

router = APIRouter(
    prefix='/auth',
    tags=['Authentication']
)


SECRET_KEY = os.environ.get("OAUTH2_SECRET_KEY")
ALGORITHM = os.environ.get("OAUTH2_ALGORITHM")
TOKEN_LIFETIME = os.environ.get("OAUTH2_ACCESS_TOKEN_EXPIRE_MINUTES")


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/login')


class UserRegisteration(BaseModel):
    username: str = Field(min_length=5, max_length=15)
    email: str = Field(min_length=10, max_length=25)
    password: str = Field(min_length=8, max_length=16)
    first_name: str = Field(min_length=3, max_length=15)
    last_name: str = Field(min_length=3, max_length=15)


class PasswordChange(BaseModel):
    current_password: str = Field(min_length=8, max_length=16)
    new_password: str = Field(min_length=8, max_length=16)
    new_password_confirm: str = Field(min_length=8, max_length=16)


class Token(BaseModel):
    access_token : str
    token_type: str


def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could Not Validate User.')
        return {'username': username, 'id': user_id, 'role': role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could Not Validate User.')
    

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(db: db_dependency, register: UserRegisteration):

    create_user = Users(
        username = register.username,
        email = register.email,
        first_name = register.first_name,
        last_name = register.last_name,
        password = bcrypt_context.hash(register.password),
        role = 'user',
        is_active = True,
    )

    db.add(create_user)
    db.commit()
    
    return register


@router.post('/login', response_model=Token)
async def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could Not Validate User.')
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=int(TOKEN_LIFETIME)))
    return {'access_token': token, 'token_type': 'bearer'}


@router.get('/user', status_code=status.HTTP_200_OK)
async def user_detail(user: user_dependency, db: db_dependency):
    user = db.query(Users).filter(Users.id == user.get('id')).first()
    return {'username': user.username, 'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name}


@router.post('/password/change', status_code=status.HTTP_200_OK)
async def change_password(user: user_dependency, db: db_dependency, change: PasswordChange):
    user = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(change.current_password, user.password):
        return HTTPException(status_code=404, detail='Wrong Password.')
    
    if change.new_password != change.new_password_confirm:
        return HTTPException(status_code=404, detail='Password Does Not Match.')
    
    user.password = bcrypt_context.hash(change.new_password)

    db.commit()
    db.refresh(user)

    return {"detail": "Password changed successfully."}
