from datetime import datetime, timedelta
from jose import JWTError, jwt
from constants import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from database import Database
from models import users
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users-login/")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_access_token(token, credentials_exception)


async def get_user_by_username(db: Database, username: str):
    query = users.select().where(users.c.username == username)
    return await db.fetch_one(query)


async def get_user_by_email(db: Database, email: str):
    query = users.select().where(users.c.email == email)
    return await db.fetch_one(query)


async def get_walker(db: Database, username: str):
    query = users.select().where(users.c.username == username)
    user = await db.fetch_one(query)
    return user['walker']


async def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_expiration: datetime = payload.get("exp")
        if token_expiration is None or datetime.utcnow() > token_expiration:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


async def authenticate_user(database: Database, username: str, password: str):
    user = await get_user_by_username(database, username)
    if not user:
        return None
    if not await verify_password(password, user['hashed_password']):
        return None
    return user
