from fastapi import FastAPI
from src.database import Base, engine

from src.routers import auth
from src.routers import todos
from src.routers import admin

from .models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get('/')
def is_running():
    return {'status': 'Running'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
