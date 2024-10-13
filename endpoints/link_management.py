from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from configuration import EndpointsList
from database import get_session
from database.crud import get_user, get_links_by_user, add_new_link
from schemas import Link, DefaultResponse, ShorterCreation
from logic import get_short, oauth2_scheme

shortener_router = APIRouter(tags=["Url"])


@shortener_router.post(EndpointsList.shortner, response_model=DefaultResponse)
async def make_shorten_link(
    url_request: ShorterCreation, session: AsyncSession = Depends(get_session)
):
    original_url = url_request.original_url
    new_url, suffix = await get_short(session)
    await add_new_link(original_url, suffix, session)
    return DefaultResponse(original_url=original_url, short_url=new_url)


@shortener_router.get("/links/", response_model=list[Link])
async def read_links(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    user = await get_user(token, session)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid authentication credentials")
    return get_links_by_user(user.id, session)


@shortener_router.delete("/links/{link_id}", response_model=dict)
async def delete_link(link_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    user = await get_user(token, session)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid authentication credentials")
    if delete_link(link_id, user.id, session):
        return {"message": "Link deleted successfully"}
    raise HTTPException(status_code=404, detail="Link not found")