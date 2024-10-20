# Shortener Webapp
This FastAPI application is designed to shorten and manage URLs. It also includes support for user authentication and authorization.

## Stack
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- JWT
- bcrypt
- PostgreSQL
- PgBouncer


## Up instruction

### 1. Clone project
```sh
git clone https://github.com/WhaleShip/BucketBot.git
```

### 2. Create .env file
```shell
make env
```

### 3. Run service
```sh
make autorun
```

#### swagger is available on [0.0.0.0:8090/swagger](http://0.0.0.0:8090/swagger)

<Br>

### To turn off the service
```sh
make off
```

<Br>

If you're experiencing issues with the PgBouncer container on Windows,
change this params in [.env](.env) <Br>
PGBOUNCER_HOST=shortener_postgres \
PGBOUNCER_PORT=5432 \
\
"If you're having troubles with container on windows, just don't use it" ©
