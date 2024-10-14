from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_session
from database.models import User
from configuration import pwd_context, oauth2_scheme, SECRET_KEY, ALGORITHM
from schemas import UserCreate




async def get_user_by_username(username: str, session: AsyncSession) -> User:
    query_result = await session.execute(
        select(User).filter(User.username == username).with_for_update()
    )
    return query_result.scalar_one_or_none()

async def create_user(user: UserCreate, session: AsyncSession):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


async def get_current_user(session: AsyncSession = Depends(get_session), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    query_result = await session.execute(
        select(User).filter(User.username == username).with_for_update()
    )
    user = query_result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    return user