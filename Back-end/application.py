
#  ------------------------------------------------------------------------------------------------
# This is the main file containing all the APIs which are having four end points to perform the CRUD operation with SQLite
#  ------------------------------------------------------------------------------------------------
from typing import List 
from starlette.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Depends, FastAPI, HTTPException, Request, Form, Response, status, File, UploadFile
from sqlalchemy.orm import Session
import crud
from security import get_password_hash,verify_password, create_access_token, verify_token, COOKIE_NAME

from crud import SendEmailVerify, UserRepository
import model
import schema
# import smtplib
from db_handler import SessionLocal, engine


model.Base.metadata.create_all(bind=engine)
IMAGEDIR = "images/"


# initiating app
app = FastAPI(
    title="Job Application",
    description="You can perform CRUD operaton",
    version="1.0.0"
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


# templating

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# path to the home/root directory

@app.get('/')
def home(request:Request):
    return templates.TemplateResponse("index.html", {"request": request})


# login/signup a user
@app.get('/signup')
def signup(request:Request):
    # jobs = db.query(model.Jobss).order_by(model.Jobss.id.desc())
    return templates.TemplateResponse("signup.html", {"request": request})


# login/signup a user
@app.post("/signupuser")
def signup_user(db:Session=Depends(get_db),name : str = Form(),username : str = Form(), email:str=Form(),password:str=Form(), cpassword:str=Form()):
    print(username)
    print(name)
    print(email)
    print(password)
    print(cpassword)
    userRepository=UserRepository(db)
    db_user= userRepository.get_user_by_username(username)
    if db_user:
        return "username is not valid"
 
    signup=model.Users(name=name, email=email,username=username,password=get_password_hash(password), cpassword=get_password_hash(cpassword))
    success=userRepository.create_user(signup)
    token=create_access_token(signup)
    SendEmailVerify.sendVerify(token)
    if success:
        return RedirectResponse(url=app.url_path_for("login"), status_code= status.HTTP_303_SEE_OTHER)
    else:
        raise HTTPException(
            status_code=401, detail="Credentials not correct"
        )
    



# login a user
@app.get('/login')
def login(request:Request):
    # jobs = db.query(model.Jobss).order_by(model.Jobss.id.desc())
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/signinuser")
def signin_user(response:Response,db:Session=Depends(get_db),username : str = Form(),password:str=Form()):
    userRepository = UserRepository(db)
    db_user = userRepository.get_user_by_username(username)
    if not db_user:
        return "username or password is not valid"
 
    if verify_password(password,db_user.password):
        token=create_access_token(db_user)
        response.set_cookie(
            key=COOKIE_NAME,
            value=token,
            httponly=True,
            expires=1800
        )
        return RedirectResponse(url=app.url_path_for("home"), status_code= status.HTTP_303_SEE_OTHER)
 
@app.get('/user/verify/{token}')
def verify_user(token,db:Session=Depends(get_db)):
    userRepository=UserRepository(db)
    payload=verify_token(token)
    username=payload.get("username")
    db_user=userRepository.get_user_by_username(username)
 
    if not username:
        raise  HTTPException(
            status_code=401, detail="Credentials not correct"
        )
    if db_user.is_active==True:
        return "your account  has been already activeed"
 
    db_user.is_active=True
    db.commit()
    response=RedirectResponse(url="/login")
    return response
    #http://127.0.0.1:8000/user/verify/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImNseWRleTAxMzEiLCJlbWFpbCI6ImNseWRleUBnbWFpbC5jb20iLCJyb2xlIjoidXNlciIsImFjdGl2ZSI6ZmFsc2V9.BKektCLzr47qn-fRtnGVulSdYlcMdemJQO_p32jWDk0


@app.get('/about')
def about(request:Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get('/contact')
def contact(request:Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@app.get('/details')
def details(request:Request):
    return templates.TemplateResponse("details.html", {"request": request})


# create a job
@app.get('/create')
def create(request:Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.post('/add')
async def create(request:Request, title:str = Form(...), role:str = Form(...), qualification:str = Form(...), town:str = Form(...), name:str = Form(...), salary:str = Form(...), description:str = Form(...), db: Session = Depends(get_db)):
    jobs = model.Jobss(title=title, role=role, qualification=qualification, town=town, name=name, salary=salary, description=description)
    db.add(jobs)
    db.commit()
    return RedirectResponse(url=app.url_path_for("list"), status_code= status.HTTP_303_SEE_OTHER)


# apply for job
@app.post('/apply', response_class=HTMLResponse)
async def apply(request:Request, email:str = Form(...), letter:str = Form(...), website:str = Form(...), name:str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    apply = model.Apply(email=email, letter=letter, website=website, name=name, file=file.filename)
    db.add(apply)
    db.commit()
    contents = await file.read()

    # save the file
    with open(f"{IMAGEDIR}{file.filename}", "wb") as f:
        f.write(contents)
    return RedirectResponse(url=app.url_path_for("list"), status_code= status.HTTP_303_SEE_OTHER)


@app.get('/testimonials')
def testimonials(request:Request):
    return templates.TemplateResponse("testimonials.html", {"request": request})

@app.get('/category')
def category(request:Request):
    return templates.TemplateResponse("category.html", {"request": request})

@app.get('/list')
def list(request:Request, db: Session = Depends(get_db)):
    jobs = db.query(model.Jobss).order_by(model.Jobss.id.desc())
    return templates.TemplateResponse("list.html", {"request": request, "jobs":jobs})







# end point to get all jobs details
@app.get('/retrieve_all_jobs_details', response_model=List[schema.Job])
def retrieve_all_jobs_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = crud.get_jobs(db=db, skip=skip, limit=limit)
    return jobs

# end point to add a new job
@app.post('/add_new_job', response_model=schema.JobAdd)
def add_new_job(job: schema.JobAdd, db: Session = Depends(get_db)):
    job_id = crud.get_job_by_job_id(db=db, job_id=job.job_id)
    if job_id:
        raise HTTPException(status_code=400, detail=f"job id {job.job_id} already exist in database: {job_id}")
    return crud.add_jobs_details_to_db(db=db, job=job)

# end point to delete a job
@app.delete('/delete_job_by_id')
def delete_job_by_id(sl_id: int, db: Session = Depends(get_db)):
    details = crud.get_job_by_id(db=db, sl_id=sl_id)
    if not details:
        raise HTTPException(status_code=404, detail=f"No record found to delete")

    try:
        crud.delete_job_details_by_id(db=db, sl_id=sl_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Unable to delete: {e}")
    return {"delete status": "success"}


# end point to update job details
@app.put('/update_job_details', response_model=schema.Job)
def update_job_details(sl_id: int, update_param: schema.UpdateJob, db: Session = Depends(get_db)):
    details = crud.get_job_by_id(db=db, sl_id=sl_id)
    if not details:
        raise HTTPException(status_code=404, detail=f"No record found to update")

    return crud.update_job_details(db=db, details=update_param, sl_id=sl_id)








 



 