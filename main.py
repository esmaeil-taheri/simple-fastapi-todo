from fastapi import FastAPI
from database import Base, engine
import models
from routers import auth
from routers import todos
from routers import admin
import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
