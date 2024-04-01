from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.staticfiles import StaticFiles
from database import metadata, database
from sqlalchemy.exc import IntegrityError
from fastapi.responses import HTMLResponse, RedirectResponse
from auth import hash_password
from auth import get_user_by_username, get_user_by_email, authenticate_user, get_current_user
from models import User, UserCreate, UserInDB, Token, LoginSchema, users

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/signup", response_class=HTMLResponse)
async def signup():
    with open('frontend/signup.html', 'r') as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.get("/login", response_class=HTMLResponse)
async def read_login():
    with open('frontend/login.html', 'r') as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token")
    return response

@app.post("/users-signup/")
async def create_user(user: UserCreate):
    user_by_username = await get_user_by_username(database, user.username)
    if user_by_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    user_by_email = await get_user_by_email(database, user.email)
    if user_by_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    try:
        hashed_password = await hash_password(user.password)
        query = users.insert().values(username=user.username, email=user.email,
                                      hashed_password=hashed_password)
        last_record_id = await database.execute(query)
        return {"id": last_record_id, "username": user.username, "email": user.email}
    except IntegrityError:
        raise HTTPException(status_code=400, detail="User already exists")


@app.post("/users-login/", response_model=Token)
async def login_for_access_token(form_data: LoginSchema):
    user = await authenticate_user(database, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/", response_class=HTMLResponse)
async def main():
    with open('frontend/main.html', 'r') as f:
        return HTMLResponse(content=f.read(), status_code=200)


app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
