from backend.auth import auth
from backend.auth.jwt_utils import gen_jwt, jwt_checker
from backend.routers import products, students
from backend.db import Base, engine
from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

# Register routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(students.router, prefix="/students", tags=["students"])
app.include_router(products.router, prefix="/product", tags=["products"])


@app.get("/gen-jwt")
def get_jwt_token():
    token = gen_jwt()
    return {"token": token}


@app.get("/", dependencies=[Depends(jwt_checker)])
def get():
    return {"data": "API working"}
