import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.encoders import jsonable_encoder

from db import get_async_db
from models import Student
from schemas import StudentCreate, StudentUpdate, StudentResponse

router = APIRouter()


@router.post("/", response_model=StudentResponse)
async def create_student(
    student: StudentCreate, db: AsyncSession = Depends(get_async_db)
):
    hashed_password = bcrypt.hashpw(student.password.encode("utf-8"), bcrypt.gensalt())
    new_student = Student(
        name=student.name, email=student.email, password=hashed_password.decode("utf-8")
    )
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return {
        "message": "Student created successfully",
        "data": jsonable_encoder(new_student),
    }


@router.get("/", response_model=StudentResponse)
async def get_all_students(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Student))
    students = result.scalars().all()
    return {
        "message": "All students retrieved successfully",
        "data": jsonable_encoder(students),
    }


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "message": "Student retrieved successfully",
        "data": jsonable_encoder(student),
    }


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student_data: StudentUpdate,
    db: AsyncSession = Depends(get_async_db),
):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if student_data.name is not None:
        student.name = student_data.name # type: ignore
    if student_data.email is not None:
        student.email = student_data.email # type: ignore

    await db.commit()
    await db.refresh(student)
    return {
        "message": "Student updated successfully",
        "data": jsonable_encoder(student),
    }


@router.delete("/{student_id}", response_model=StudentResponse)
async def delete_student(student_id: int, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalar_one_or_none()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    await db.delete(student)
    await db.commit()
    return {
        "message": "Student deleted successfully",
        "data": {},
    }
