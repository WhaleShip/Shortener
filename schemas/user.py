from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    username: str

    model_config = ConfigDict(from_attributes=True)
