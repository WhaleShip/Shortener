from os import environ

from pydantic_settings import BaseSettings


class ServiceSettings(BaseSettings):
    APP_HOST: str = environ.get("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(environ.get("APP_PORT", 8080))

    POSTGRES_DB: str = environ.get("POSTGRES_DB", "shortener_db")
    PGBOUNCER_HOST: str = environ.get("POSTGRES_HOST", "localhost")
    PGBOUNCER_PORT: int = int(environ.get("POSTGRES_PORT", "5432")[-4:])
    POSTGRES_USER: str = environ.get("POSTGRES_USER", "user")
    POSTGRES_PASSWORD: str = environ.get("POSTGRES_PASSWORD", "pass")
