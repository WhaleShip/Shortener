from sqlalchemy import Column, Integer, String

from database import BaseDeclarativeModel


class Link(BaseDeclarativeModel):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    suffix = Column(String, unique=True, index=True)
