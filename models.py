from sqlalchemy import Column, Integer, String, Table
from database import metadata
from pydantic import BaseModel

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50)),
    Column("email", String(50)),
    Column("hashed_password", String(100)),
)


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginSchema(BaseModel):
    username: str
    password: str


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    username: str
    email: str


class UserInDB(User):
    hashed_password: str
