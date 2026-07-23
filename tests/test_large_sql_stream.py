import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService


@pytest.mark.asyncio
async def test_large_sql_stream():

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

    total_rows = 0

    async for batch in db.sql.stream(
        "select * from generate_series(1,100000) id"
    ):
        total_rows += len(batch)

    assert total_rows == 100000