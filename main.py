from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from databases import Database
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from datetime import datetime, timedelta
from jose import JWTError, jwt
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from database import metadata, database
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError

# Constants and Security

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Database setup

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class User(BaseModel):
    username: str
    email: str


class UserInDB(User):
    hashed_password: str


# Dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Application and Router
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
router = APIRouter()

users = Table(
    "users", metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50)),
    Column("email", String(50)),
    Column("hashed_password", String(100)),
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(db: Database, username: str):
    query = users.select().where(users.c.username == username)
    return await db.fetch_one(query)



# @router.post("/token")
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = await get_user(database, form_data.username)
#     if not user or not verify_password(form_data.password, user["hashed_password"]):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user["username"]}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

@app.get("/routes")
async def get_routes():
    return [{"path": route.path, "methods": route.methods} for route in app.routes]
@app.post("/users")
async def create_user(user: UserCreate):
    try:
        query = users.insert().values(username=user.username, email=user.email, hashed_password=get_password_hash(user.password))
        last_record_id = await database.execute(query)
        return {"id": last_record_id, "username": user.username, "email": user.email}
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")


app.include_router(router)
