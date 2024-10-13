ENV_FILE = .env

MAKEFILE_DIR = $(shell readlink -f $(shell dirname $(lastword $(MAKEFILE_LIST))))

CORRECT_PYTHONPATH = $(MAKEFILE_DIR)


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

run:
	@chmod +x scripts/pgbouncer/entrypoint.sh
	@docker compose up --build -d

off:
	@docker compose down

revision:
	@cd database && PYTHONPATH=$(CORRECT_PYTHONPATH) alembic revision --autogenerate

migrate:
	cd database && PYTHONPATH=$(CORRECT_PYTHONPATH) alembic upgrade head
