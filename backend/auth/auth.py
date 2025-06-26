import bcrypt
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, HTTPException

from backend.auth.jwt_utils import gen_jwt
from backend.db import get_async_db
from backend.models import Student
from backend.schemas import LoginRequest, StudentCreate, StudentResponse


router = APIRouter()

student_cache = {}

@router.post("/login")
async def student_login(
    stuendLoginReq: LoginRequest,
    db: AsyncSession = Depends(get_async_db),
):
    email = stuendLoginReq.email

    # Check cache first
    student = student_cache.get(email)
    if not student:
        result = await db.execute(select(Student).where(Student.email == email))
        student = result.scalar_one_or_none()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        student_cache[email] = student

    if not bcrypt.checkpw(stuendLoginReq.password.encode("utf-8"), student.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Password Wrong")

    token = gen_jwt({"user": student.email})
    return {
        "message": "Login successful",
        "token": jsonable_encoder(token),
    }


@router.post("/signup", response_model=StudentResponse)
async def create_student(
    student: StudentCreate,
    db: AsyncSession = Depends(get_async_db),
):
    try:
        hashed_password = bcrypt.hashpw(student.password.encode("utf-8"), bcrypt.gensalt())
        new_student = Student(
            name=student.name,
            email=student.email,
            password=hashed_password.decode("utf-8")
        )

        db.add(new_student)
        await db.commit()
        await db.refresh(new_student)

        # Invalidate cache
        student_cache.pop(student.email, None)

        return {
            "message": "Student created successfully",
            "data": jsonable_encoder(new_student),
        }
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Error creating student")
