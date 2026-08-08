from sqlalchemy import create_engine
from config.config import settings 
from sqlalchemy import create_engine

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)