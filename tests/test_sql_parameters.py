import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService


@pytest.mark.asyncio
async def test_sql_parameters():

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
        """
        SELECT
            $1::integer + $2::integer
            AS result;
        """,
        10,
        20,
    )

    assert len(rows) == 1
    assert rows[0]["result"] == 30
