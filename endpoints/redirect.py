from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette import status

from configuration import EndpointsList
from database import get_session
from database.models import Link

redirect_router = APIRouter(tags=["Url"])


@redirect_router.get(
    path=EndpointsList.redirect + "/{suffix}",
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "URL `request.url` doesn't exist"}
    },
)
async def get_link(suffix: str, session: AsyncSession = Depends(get_session)):
    query_result = await session.execute(
        select(Link).filter(Link.suffix == suffix).with_for_update()
    )
    link = query_result.scalar_one_or_none()

    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(link.url)
