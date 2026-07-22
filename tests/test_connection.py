import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database import DatabaseService


@pytest.mark.asyncio
async def test_postgresql_connection():

    settings = Settings()

    pool = PostgresPool()

    await pool.connect(
        host=settings.pg_host,
        port=settings.pg_port,
        database=settings.pg_database,
        user=settings.pg_user,
        password=settings.pg_password,
    )

    db = DatabaseService(pool)

    rows = await db.sql.execute(
        "select version();"
    )

    assert len(rows) == 1

    version = rows[0]["version"]

    assert version is not None
    assert "PostgreSQL" in version