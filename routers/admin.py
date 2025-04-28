from fastapi import Depends, Path, HTTPException, APIRouter

from typing import Annotated
from src.database import SessionLocal
from sqlalchemy.orm import Session 
from starlette import status

from src.models import Todos
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)


def get_db():
    db = SessionLocal()
    try :
        yield db
    finally :
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/todos', status_code=status.HTTP_200_OK)
async def todos_list(user: user_dependency, db: db_dependency):
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permision Denied.')
    todos = db.query(Todos).all()
    return todos


@router.delete('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Permision Denied.')
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail='Todo Not Found.')

    db.query(Todos).filter(Todos.id == todo_id).delete()
    # db.delete(todo)
    db.commit()

