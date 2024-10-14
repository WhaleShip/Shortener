import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from uvicorn import run

from configuration import ServiceSettings
from endpoints import routers


def get_configured_app() -> FastAPI:
    application = FastAPI(
        title="Shortener",
        docs_url="/swagger",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for r in routers:
        application.include_router(r)

    return application


app = get_configured_app()


if __name__ == "__main__":
    config = ServiceSettings()
    run(
        app="main:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True,
        reload_dirs=[os.path.basename(os.path.dirname(__file__))],
    )
