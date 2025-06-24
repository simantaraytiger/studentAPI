import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from auth.jwt_utils import gen_jwt
from models import Student
from routers.students import get_db
from schemas import LoginRequest


router = APIRouter()


@router.post("/login")
def student_login(stuendLoginReq: LoginRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.email == stuendLoginReq.email).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    studentData = jsonable_encoder(student)

    if not bcrypt.checkpw(stuendLoginReq.password.encode("utf-8"), student.password.encode("utf-8")):
        raise HTTPException(status_code=404, detail="Password Worng")
    token = gen_jwt({"user": studentData["email"]})
    return {
        "message": "Login successful",
        "token": jsonable_encoder(token),
    }
