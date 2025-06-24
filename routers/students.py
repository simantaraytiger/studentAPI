from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from db import SessionLocal
from models import Student
from schemas import StudentCreate, StudentUpdate, StudentOut, StudentResponse

router = APIRouter()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(
        name=student.name, email=student.email, password=student.password
    )
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return {
        "message": "Student created successfully",
        "data": jsonable_encoder(new_student),
    }


@router.get("/", response_model=StudentResponse)
def get_all_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    return {
        "message": "All students retrieved successfully",
        "data": jsonable_encoder(students),
    }


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return {
        "message": "Student retrieved successfully",
        "data": jsonable_encoder(student),
    }


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int, student_data: StudentUpdate, db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if student_data.name is not None:
        student.name = student_data.name  # type: ignore
    if student_data.email is not None:
        student.email = student_data.email  # type: ignore

    db.commit()
    db.refresh(student)
    return {
        "message": "Student updated successfully",
        "data": jsonable_encoder(student),
    }


@router.delete("/{student_id}", response_model=StudentResponse)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(student)
    db.commit()
    return {"message": "Student deleted successfully", "data": {}}
