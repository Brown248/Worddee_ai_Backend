from sqlalchemy import create_engine, MetaData
from databases import Database
from app.config import settings

DATABASE_URL = settings.DATABASE_URL

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)
