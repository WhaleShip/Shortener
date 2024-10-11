from os import environ

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from utils.singleton import singleton


database = environ.get("POSTGRES_DB", "shortner_postgres")
user =  environ.get("POSTGRES_USER", "user")
password =  environ.get("POSTGRES_PASSWORD", "pass")
host =  environ.get("PGBOUNCER_HOST", "shortner_pgbouncer")
port = environ.get("PGBOUNCER_PORT", "6432")



@singleton
class SessionManager:
    def __init__(self) -> None:
        self.engine = create_async_engine(f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}", echo=True, future=True)

    def get_session_maker(self) -> sessionmaker:
        return sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    session_maker = SessionManager().get_session_maker()
    async with session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
