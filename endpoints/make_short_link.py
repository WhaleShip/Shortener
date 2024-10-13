from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from database.models import Link
from configuration import EndpointsList
from schemas.link import ShorterCreation, DefaultResponse
from logic import get_short

shortener_router = APIRouter(tags=["Url"])

@shortener_router.post(EndpointsList.shortner, response_model=DefaultResponse)
async def make_shorten_link(url_request: ShorterCreation, session: AsyncSession = Depends(get_session)):
    original_url = url_request.original_url
    new_url, suffix = await get_short(session) 
    new_link = Link(url=original_url, suffix=suffix)

    session.add(new_link)
    await session.commit()
    await session.refresh(new_link)
    return DefaultResponse(original_url=original_url, short_url=new_url)