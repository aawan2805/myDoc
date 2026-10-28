"""Crea la extensión vector y las tablas. Es nuestro 'manage.py migrate' provisional
hasta que entre Alembic.

Uso:
    uv run python -m app.db.setup
"""
from sqlalchemy import text
from sqlmodel import SQLModel

from app.db.db import engine
from app.utils.logger import AppLogger

log = AppLogger("setup")


def setup_db():
    # La extensión no se puede crear con el ORM, es la única línea de SQL
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    SQLModel.metadata.create_all(engine)
    log.ok("Tablas listas")


if __name__ == "__main__":
    setup_db()
