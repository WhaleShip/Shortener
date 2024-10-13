from fastapi import APIRouter

from database import get_session
from database.models import Link
from configuration import EndpointsList
from schemas.link import ShorterCreation, DefaultResponse

shortener_router = APIRouter(tags=["Url"])

@shortener_router.post(EndpointsList.shortner, response_model=DefaultResponse)
async def shorten_link(url_request: ShorterCreation):
    original_url = url_request.original_url
    shortened_url = original_url.split("//")[-1].replace("/", "-")
    new_link = Link(url=original_url, suffix=shortened_url)
    async with get_session() as session:
        await session.add(new_link)
        await session.commit()
        await session.refresh(new_link)
    return ShorterCreation(original_url=original_url.original_url)