from databases import Database
from sqlalchemy import create_engine, MetaData
from constants import DATABASE_URL

database = Database(DATABASE_URL)
metadata = MetaData()

