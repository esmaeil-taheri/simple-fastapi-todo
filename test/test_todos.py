from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from src.database import Base
from src.main import app
from src.routers.todos import get_current_user, get_db
from src.models import Todos

from fastapi.testclient import TestClient
from fastapi import status

import pytest


SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {'username': 'esi', 'id': 1, 'role': 'admin'}

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title = 'Test-1',
        description='Test-desc',
        priority=5,
        complete=False,
        user=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text('DELETE FROM todos;'))
        connection.commit()


def test_todos_list_authenticated(test_todo):
    response = client.get('todos/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete': False, 'title': 'Test-1', 
                                'description': 'Test-desc', 'id': 1, 
                                'priority': 5, 'user': 1}]
    

def test_todo_detail_authenticated(test_todo):
    response = client.get('todos/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False, 'title': 'Test-1', 
                                'description': 'Test-desc', 'id': 1, 
                                'priority': 5, 'user': 1}
    

def test_todo_detail_authenticated_not_found(test_todo):
    response = client.get('todos/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo Not Found.'}

