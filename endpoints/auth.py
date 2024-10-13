from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from database.crud import get_user, create_user
from database.crud.users import pwd_context
from database.session_manager import password
from schemas import User
from schemas import UserCreate

auth_router = APIRouter(tags=["Url"])

@auth_router.post("/register", response_model=User)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    db_user = await get_user(user.username, session)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = await create_user(user, session)
    return User(username=new_user.username)

async def authenticate_user(session: AsyncSession, username: str, password: str):
    user = await get_user(username, session)
    if not user or not pwd_context.verify(password, user.hashed_password):
        return None
    return user

@auth_router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user.username, "token_type": "bearer"}