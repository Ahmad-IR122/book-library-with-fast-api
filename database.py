from sqlalchemy import create_engine
from config.config import settings 
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)


class BaseModel(DeclarativeBase):
    pass