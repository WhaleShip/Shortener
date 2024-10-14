from pydantic import BaseModel, ConfigDict


class LinkResponse(BaseModel):
    id: int
    url: str
    suffix: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class ShorterCreation(BaseModel):
    original_url: str
