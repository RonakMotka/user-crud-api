from typing import List
from pydantic import BaseModel, validator, Field
from fastapi import HTTPException, status
from email_validator import EmailNotValidError, validate_email


class UserAdd(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    @validator("email")
    def email_valid(cls, email):
        try:
            valid = validate_email(email)
            return valid.email
        except EmailNotValidError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e)


class UserLogin(BaseModel):
    email: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=3, max_length=50)

    @validator("email")
    def valid_email(cls, email):
        try:
            valid = validate_email(email)
            return valid.email
        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
            )


class User(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=60)
    last_name: str = Field(..., min_length=2, max_length=60)


class UserList(BaseModel):
    count: int
    list: List[User] = []

    class Config:
        orm_mode = True
