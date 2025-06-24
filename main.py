from fastapi import Depends, FastAPI, Request
from auth import auth
from auth.jwt_utils import gen_jwt, jwt_checker
from db import engine
from models import Base
from routers import students

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# # Register router
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(students.router, prefix="/students", tags=["students"])


@app.get("/gen-jwt")
def get_jwt_token():
    token = gen_jwt()
    return {"token": token}


@app.get("/", dependencies=[Depends(jwt_checker)])
def get():
    return {"data": "Api working"}
