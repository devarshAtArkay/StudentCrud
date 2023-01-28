from pydantic import BaseModel, Field, validator
from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException, status
from models import GenderEnum, StreamEnum

from typing import List

# A base schema model for creating student
class StudentBase(BaseModel):

    first_name: str = Field(default=None, min_length=3, max_length=50)
    last_name: str = Field(default=None, min_length=3, max_length=50)
    email: str = Field(default=None, min_length=3, max_length=50)
    password: str = Field(min_length=3, max_length=50)
    roll_no: str = Field(default=None, min_length=1, max_length=10)
    gender: GenderEnum
    phone_num:str = Field(min_length=10,max_length=13)
    class_no: int = Field(default=None)
    streams: StreamEnum

    # validating email using email validator
    @validator("email")
    def valid_email(cls, email):
        try:
            if email == "" or email == None:
                return email
            else:
                valid = validate_email(email)
                return valid.email
        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
            )


# A login schema
class StudentLogin(BaseModel):

    email: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=3, max_length=50)


# A response schema for login
class StudentLoginResponse(BaseModel):
    id: str = Field(min_length=36, max_length=36)
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=3, max_length=50)
    email: str
    token: str

    class Config:
        orm_mode = True


# A schema which will be used to show students
class StudentShow(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    roll_no: str
    gender: GenderEnum
    phone_num:str = None
    class_no: int

    class Config:

        orm_mode = True


# A schema for list of StudentShow schema and its count
class StudentList(BaseModel):
    count: int
    list: List[StudentShow]

    class Config:
        orm_mode = True


# An update schema
class StudentUpdate(BaseModel):

    first_name: str = Field(default=None, min_length=3, max_length=50)
    last_name: str = Field(default=None, min_length=3, max_length=50)
    email: str = Field(default=None, min_length=3, max_length=50)
    gender: GenderEnum
    phone_num:str = Field(min_length=10,max_length=13)
    class_no: int = Field(default=None)
    streams: StreamEnum
    # validating email using email validator
    @validator("email")
    def valid_email(cls, email):
        try:
            if email == "" or email == None:
                return email
            else:
                valid = validate_email(email)
                return valid.email
        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
            )
