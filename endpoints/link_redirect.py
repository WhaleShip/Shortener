from fastapi import APIRouter, HTTPException

from database import get_session
from configuration import EndpointsList
from database.models import Link
from schemas import DefaultResponse

redirect_router = APIRouter(tags=["Url"])

@redirect_router.get(path=EndpointsList.shortner+"{shortened_url}", response_model=DefaultResponse)
async def get_link(shortened_url: str):
    with get_session() as db:
        link = db.query(Link).filter(Link.shortened_url == shortened_url).first()
        if link is None:
            raise HTTPException(status_code=404, detail="Link not found")
    return link