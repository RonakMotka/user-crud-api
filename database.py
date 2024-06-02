from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import config


SQLALCHEMY_DATABASE_URL = (
    "mysql+pymysql://"
    +config["db_user"]
    +":"
    +config["db_pass"]
    +"@"
    +config["db_host"]   
    +"/"
    +config["db_name"]
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()