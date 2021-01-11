from typing import List

from pydantic import BaseModel


class Student(BaseModel):
    name: str
    phone_number: str
    address: str
    mail: str
    sex: str

    class Config:
        orm_mode = True


class StudentGroup(BaseModel):
    count: int
    limit: int
    offset: int
    data: List[Student]
