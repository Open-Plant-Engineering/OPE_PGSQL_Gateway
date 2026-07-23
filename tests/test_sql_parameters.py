import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService


@pytest.mark.asyncio
async def test_sql_parameters(database_service):

    rows = await database_service.sql.execute(
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
