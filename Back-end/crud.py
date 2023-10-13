
#  -------------------------------------------------------------------------------
#  Here the Crud.py file contains all the method for CRUD operation
#  -------------------------------------------------------------------------------

from sqlalchemy.orm import Session
import model 
import schema 

from model import Users
from typing import  Dict,Any
 
import smtplib
from email.message import EmailMessage


def get_job_by_job_id(db: Session, job_id: str):
    return db.query(model.Jobs).filter(model.Jobs.job_id == job_id).first()


def get_job_by_id(db: Session, sl_id: int):
    return db.query(model.Jobs).filter(model.Jobs.id == sl_id).first()


def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Jobs).offset(skip).limit(limit).all()


def add_jobs_details_to_db(db: Session, job: schema.JobAdd):
    jb_details = model.Jobs(
        job_id=job.job_id,
        job_title=job.job_title,
        job_role=job.job_role,
        qualifications=job.qualifications,
        town=job.town,
        job_description=job.job_description
    )
    db.add(jb_details)
    db.commit()
    db.refresh(jb_details)
    return model.Jobs(**job.dict())
 

def update_job_details(db: Session, sl_id: int, details: schema.UpdateJob):
    db.query(model.Jobs).filter(model.Jobs.id == sl_id).update(vars(details))
    db.commit()
    return db.query(model.Jobs).filter(model.Jobs.id == sl_id).first()


def delete_job_details_by_id(db: Session, sl_id: int):
    try:
        db.query(model.Jobs).filter(model.Jobs.id == sl_id).delete()
        db.commit()
    except Exception as e:
        raise Exception(e)
    






 
class UserRepository:
    def __init__(self,sess:Session):
        self.sess: Session=sess
 
    def create_user(self,signup:Users) -> bool:
         try:
             self.sess.add(signup)
             self.sess.commit()
         except:
             return False
         return True
 
    def get_user(self):
        return  self.sess.query(Users).all()
 
    def get_user_by_username(self,username:str):
        return self.sess.query(Users).filter(Users.username==username).first()
 
    def update_user(self,id:int,details:Dict[str,Any]) -> bool:
        try:
            self.sess.query(Users).filter(Users.id==id).update(details)
            self.sess.commit()
        except:
            return False
        return True
    def delete_user(self,id:int)-> bool:
        try:
            self.sess.query(Users).filter(Users.id==id).delete()
            self.sess.commit()
        except:
            return  False
        return  True
 
class SendEmailVerify:
 
  def sendVerify(token):
    email_address = "brandontenengble8@gmail.com" # type Email
    email_password = "awcexagulhjzjqdo" # If you do not have a gmail apps password, create a new app with using generate password. Check your apps and passwords https://myaccount.google.com/apppasswords
 
    # create email
    msg = EmailMessage()
    msg['Subject'] = "Email subject"
    msg['From'] = email_address
    msg['To'] = "sandjonggrace74@gmail.com" # type Email
    msg.set_content(
       f"""\
    verify account        
    http://localhost:8080/user/verify/{token}
    """,
         
    )
    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
