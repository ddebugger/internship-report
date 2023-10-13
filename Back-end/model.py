
#  --------------------------------------------------------------------------------------------
# A data model in a database should be relational which means it is described by tables.
# The data describes how the data is stored and organized.
# A data model may belong to one or more schemas, usually, it just belongs to one schema
#  --------------------------------------------------------------------------------------------
from fastapi import UploadFile
from sqlalchemy import Boolean, Column, Integer, String, LargeBinary, Enum
from db_handler import Base
from schema import Roles

  
class Jobs(Base):  
    __tablename__ = "job"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    job_id = Column(String, unique=True, index=True, nullable=False)
    job_title = Column(String(255), index=True, nullable=False)
    job_role = Column(String(100), index=True, nullable=False)
    qualifications = Column(String, index=True, nullable=False)
    # membership_required = Column(Boolean, nullable=False, default=True)
    town = Column(String(255), index=True, nullable=False)
    job_description = Column(String, index=True)


 
class Jobss(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    role = Column(String(200))
    qualification = Column(String(300))
    town = Column(String(200))
    name = Column(String(200))
    salary = Column(String(200))
    description = Column(String(800))

    def __repr__(self):
        return '<Jobss %r>' % (self.id)
    

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), unique=True, index=True)
    email = Column(String(200), unique=True, index=True)
    username = Column(String(200), unique=True, index=True)
    password = Column(String(200), unique=False, index=True)
    cpassword = Column(String(200), unique=False, index=True)
    is_active=Column(Boolean,default=False)
    role=Column(Enum(Roles),default="user")

    def __repr__(self):
        return '<Users %r>' % (self.id)
    

class Apply(Base):
    __tablename__ = 'apply'

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    email = Column(String(200))
    letter = Column(String(200))
    website = Column(String(200))
    file = Column(String(400) )
    