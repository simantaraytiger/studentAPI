from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List, Union


class StudentCreate(BaseModel):
    name: str
    email: str
    password: str


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
    email: str
    password: str


# make a seprate file


class ProductCreate(BaseModel):
    name: str
    price: float
    description: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None


class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str]
    date_added: datetime

    class Config:
        orm_mode = True


class ProductResponse(BaseModel):
    message: str
    data: Union[ProductOut, List[ProductOut]]
