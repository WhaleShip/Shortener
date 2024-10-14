from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import BaseDeclarativeModel


class User(BaseDeclarativeModel):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    links = relationship("Link", back_populates="owner")
