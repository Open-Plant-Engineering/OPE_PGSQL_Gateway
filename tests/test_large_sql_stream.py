import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService


@pytest.mark.asyncio
async def test_large_sql_stream(database_service):

    total_rows = 0

    async for batch in database_service.sql.stream(
        "select * from generate_series(1,100000) id"
    ):
        total_rows += len(batch)

    assert total_rows == 100000