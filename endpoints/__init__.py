from endpoints.auth import auth_router
from endpoints.link_redirect import redirect_router
from endpoints.make_short_link import shortener_router

routers = [shortener_router, redirect_router, auth_router]

__all__ = [
    "routers",
]
