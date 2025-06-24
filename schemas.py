from pydantic import BaseModel
from typing import Optional, List, Union


class StudentCreate(BaseModel):
    name: str
    email: str
    password:str


class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class StudentOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class StudentResponse(BaseModel):
    message: str
    data: Union[StudentOut, List[StudentOut]]

class LoginRequest(BaseModel):
    email:str
    password:str