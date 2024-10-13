from sqlalchemy.orm import Session

from database.models import Link


def get_links_by_user(session: Session, user_id: int):
    return session.query(Link).filter(Link.owner_id == user_id).all()