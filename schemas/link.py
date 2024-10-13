from pydantic import BaseModel


class ShorterCreation(BaseModel):
    original_url: str

class DefaultResponse(BaseModel):
    original_url: str
    short_url: str

    class Config:
        orm_mode = True