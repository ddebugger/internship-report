
#  ---------------------------------------------------------------------------
#  the db_handler.py file takes care in Handling database
#  ---------------------------------------------------------------------------
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# creating engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./job_database.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A simple constructor that  allows initialization from kwargs.
Base = declarative_base()
 