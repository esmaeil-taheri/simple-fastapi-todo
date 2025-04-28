from fastapi import Depends, Path, HTTPException, APIRouter

from typing import Annotated
from src.database import SessionLocal
from sqlalchemy.orm import Session 
from pydantic import BaseModel, Field
from starlette import status

from src.models import Todos
from .auth import get_current_user


router = APIRouter(
    prefix='/todos',
    tags=['Todos']
)


def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=10, max_length=300)
    priority: int = Field(gt=0, lt=6)
    complete: bool


@router.get('/', status_code=status.HTTP_200_OK)
async def todos_list(user: user_dependency, db: db_dependency):
    return db.query(Todos).filter(Todos.user == user.get('id')).all()


@router.get('/todo/{todo_id}', status_code=status.HTTP_200_OK)
async def todo_detail(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.user == user.get('id')).first()
    if todo is not None:
        return todo
    raise HTTPException(status_code=404, detail='Todo Not Found.')


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    todo = Todos(**todo_request.model_dump(), user=user.get('id'))
    db.add(todo)
    db.commit()
    return todo_request


@router.put('/{todo_id}', status_code=status.HTTP_200_OK)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.user == user.get('id')).first()
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo Not Found.')
    
    todo.title = todo_request.title
    todo.description = todo_request.description
    todo.priority = todo_request.priority
    todo.complete = todo_request.complete

    db.add(todo)
    db.commit()
    return todo_request


@router.delete('/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    todo = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.user == user.get('id')).first()
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo Not Found.')

    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.user == user.get('id')).delete()
    db.commit()
