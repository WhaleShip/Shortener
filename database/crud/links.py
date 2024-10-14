from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Link, User


async def get_links_by_user(user_id: int, session: AsyncSession):
    query_result = await session.execute(
        select(Link).filter(Link.owner_id == user_id).with_for_update()
    )
    return query_result.scalars().all()


async def add_new_link(original_url, suffix, session: AsyncSession, owner: User):
    new_link = Link(url=original_url, suffix=suffix, owner_id=owner.id, owner=owner)

    session.add(new_link)
    await session.commit()
    await session.refresh(new_link)


async def delete_link(
    link_suffix: str,
    owner_id: int,
    session: AsyncSession,
):
    query_result = await session.execute(
        select(Link)
        .filter(Link.suffix == link_suffix, Link.owner_id == owner_id)
        .with_for_update()
    )
    link = query_result.scalar_one_or_none()
    if link:
        await session.delete(link)
        await session.commit()
        return True
    return False
