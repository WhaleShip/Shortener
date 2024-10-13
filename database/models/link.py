from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import BaseDeclarativeModel


class Link(BaseDeclarativeModel):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True)
    suffix = Column(String, unique=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.id'))

    owner = relationship("User", back_populates="links")

