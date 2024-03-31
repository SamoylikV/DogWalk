from sqlalchemy import Column, Integer, String, Table
from database import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50)),
    Column("email", String(50)),
    Column("hashed_password", String(100)),
)