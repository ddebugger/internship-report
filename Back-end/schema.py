
#  --------------------------------------------------------------------------------
# the schema.py file is a collection of database objects that are logically grouped together.
# These can be anything, tables, views, stored procedure etc.
# Schemas are typically used to logically group objects in a database.
#  ---------------------------------------------------------------------------------
from typing import Optional
from datetime import date
from pydantic import BaseModel, EmailStr
from enum import Enum


class JobBase(BaseModel):
    job_title: str
    job_role: str
    qualifications: str
    town: str


class JobAdd(JobBase):
    job_id: str
    job_description: Optional[str] = None
    class Config:
        orm_mode = True


class Job(JobAdd):
    id: int
    class Config:
        orm_mode = True


class UpdateJob(BaseModel):
    job_description: Optional[str] = None
    class Config:
        orm_mode = True


class UserSchema(BaseModel):
    name: str
    email: EmailStr
    username: str
    password: str
    cpassword: str

    class Config:
        orm_mode = True

class Roles(Enum):
    user = "user"
    admin = "admin"