from random import choice
from string import ascii_uppercase, digits

from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession

from configuration import ServiceSettings
from database.models import Link
from configuration import EndpointsList


async def get_short(session: AsyncSession):
    config = ServiceSettings()
    while True:
        suffix = "".join(choice(ascii_uppercase + digits) for _ in range(8))
        exist_query = select(exists().where(Link.suffix == suffix))
        exist = await session.scalar(exist_query)
        if not exist:
            break

    short_url = f"{config.APP_HOST}:{config.APP_PORT}{EndpointsList.redirect}/{suffix}"
    return short_url, suffix