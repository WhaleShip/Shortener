ENV_FILE = .env

MAKEFILE_DIR = $(shell readlink -f $(shell dirname $(lastword $(MAKEFILE_LIST))))

PROJECT_PATH = $(MAKEFILE_DIR)

VENV_PATH = $(PROJECT_PATH)/venv


ENV_VARS = \
	APP_HOST=0.0.0.0 \
	APP_PORT=8080 \
    POSTGRES_DB=shortener_postgres \
    POSTGRES_USER=user \
    POSTGRES_PASSWORD=pass \
    POSTGRES_HOST=db \
    POSTGRES_PORT=5432 \
	PGBOUNCER_HOST=shortener_pgbouncer \
	PGBOUNCER_PORT=6432

env:
	@$(eval SHELL:=/bin/bash)
	@printf "%s\n" $(ENV_VARS) > $(ENV_FILE)
	@echo "$(ENV_FILE) file created"

db:
	@docker compose up --build -d db pgbouncer

run-app:
	@docker compose up --build -d app

off-app:
	@docker compose down app

autorun:
	@chmod +x scripts/pgbouncer/entrypoint.sh
	@docker compose up --build -d
	@make migrate

off:
	@docker compose down

revision:
	@cd database && PYTHONPATH=$(PROJECT_PATH) $(VENV_PATH)/bin/alembic revision --autogenerate

migrate:
	cd database && PYTHONPATH=$(PROJECT_PATH) $(VENV_PATH)/bin/alembic upgrade head
