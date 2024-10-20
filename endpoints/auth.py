from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from configuration import ACCESS_TOKEN_EXPIRE_MINUTES, EndpointsList
from database import get_session
from database.crud import create_user, get_user_by_username
from logic import create_access_token, verify_password
from schemas import Token, User, UserCreate

auth_router = APIRouter(tags=["Url"])


@auth_router.post(EndpointsList.registration)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)):
    db_user = await get_user_by_username(user.username, session)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = await create_user(user, session)
    return {"message": f"User {new_user.username} registered successfully"}


async def authenticate_user(username: str, password: str, session):
    user = await get_user_by_username(username, session)
    if user is None or not verify_password(password, user.hashed_password):
        return False
    return user


@auth_router.post(EndpointsList.login, response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
