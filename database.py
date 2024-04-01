from databases import Database
from sqlalchemy import create_engine, MetaData
from constants import DATABASE_URL

ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)

database = Database(ASYNC_DATABASE_URL)
metadata = MetaData()
