import os
import urllib.parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Url encode evironmental variables
USER = urllib.parse.quote(os.environ['POSTGRES_USER'])
PASSWORD = urllib.parse.quote(os.environ['POSTGRES_PASSWORD'])
DB_NAME = urllib.parse.quote(os.environ['POSTGRES_DB'])

SQLALCHEMY_DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@postgres/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()