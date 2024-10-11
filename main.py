import os

from fastapi import FastAPI
from uvicorn import run

def get_app() -> FastAPI:
    application = FastAPI(
        title="Shortener",
        docs_url="/swagger",
    )
    return application


app = get_app()


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    run(
        app="main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        reload_dirs=[os.path.basename(os.path.dirname(__file__))],
    )
