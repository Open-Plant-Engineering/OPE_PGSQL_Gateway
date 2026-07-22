import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database import DatabaseService


@pytest.mark.asyncio
async def test_function_not_found():

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

    with pytest.raises(Exception):

        await db.function.execute(
            "public",
            "function_that_does_not_exist",
        )