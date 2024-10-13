import os

from fastapi import FastAPI
from uvicorn import run
from endpoints import routers



def get_configured_app() -> FastAPI:
    application = FastAPI(title="Shortener",
                          docs_url="/swagger",)
    for r in routers:
        application.include_router(r)

    return application


app = get_configured_app()


if __name__ == "__main__":
    run(
        app="main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        reload_dirs=[os.path.basename(os.path.dirname(__file__))],
    )
