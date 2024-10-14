from alembic import command
from alembic.config import Config


def run_migrations():
    # Создаем объект конфигурации Alembic
    alembic_cfg = Config("database/alembic.ini")

    alembic_cfg.set_main_option("script_location", "database/alembic")

    command.upgrade(alembic_cfg, "head")


if __name__ == "__main__":
    run_migrations()
