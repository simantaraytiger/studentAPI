from fastapi import FastAPI
from db import engine
from models import Base
from routers import students

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# # Register router
app.include_router(students.router, prefix="/students", tags=["students"])

app.get("/")
def get():
    return {"data":"hey"}