
from pydantic import BaseModel

class Link(BaseModel):
    id: int
    url: str
    short_url: str
    owner_id: int

    class Config:
        orm_mode = True

class ShorterCreation(BaseModel):
    original_url: str


class DefaultResponse(BaseModel):
    original_url: str
    short_url: str

    class Config:
        orm_mode = True
