from endpoints.auth import auth_router
from endpoints.link_management import shortener_router
from endpoints.redirect import redirect_router

routers = [shortener_router, redirect_router, auth_router]

__all__ = [
    "routers",
]
