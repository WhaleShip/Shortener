from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User
from logic import pwd_context
from schemas import UserCreate




async def get_user(username: str, session: AsyncSession) -> User:
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
