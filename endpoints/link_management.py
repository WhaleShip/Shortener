from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from configuration import EndpointsList
from database import get_session
from database.crud import add_new_link, delete_link, get_links_by_user
from database.crud.users import get_current_user
from database.models import Link, User
from logic import get_short
from schemas import LinkResponse, ShorterCreation

shortener_router = APIRouter(tags=["Url"])


@shortener_router.post(EndpointsList.shortner)
async def create_shorten_link(
    url_request: ShorterCreation,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    original_url = url_request.original_url
    new_url, suffix = await get_short(session)
    await add_new_link(original_url, suffix, session, current_user)

    return {"original_url": original_url, "short_url": new_url}


def convert_link_to_schema(link: Link) -> LinkResponse:
    return LinkResponse(
        id=link.id, url=link.url, suffix=link.suffix, owner_id=link.owner_id
    )


def convert_links_to_schemas(links: List[Link]) -> List[LinkResponse]:
    return [convert_link_to_schema(link) for link in links]


@shortener_router.get("/links/", response_model=list[LinkResponse])
async def get_user_links(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    db_links = await get_links_by_user(current_user.id, session)
    return convert_links_to_schemas(db_links)


@shortener_router.delete("/links/{link_suffix}", response_model=dict)
async def delete_link_endpoint(
    link_suffix: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    deleted = await delete_link(link_suffix, current_user.id, session)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link not found or not owned by user.",
        )

    return {"message": "Link deleted successfully"}
