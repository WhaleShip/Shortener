from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from logic.get_short_link import get_short

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

__all__ = [
    "get_short",
    "oauth2_scheme",
    "pwd_context"
]
