import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService


@pytest.mark.asyncio
async def test_invalid_sql(database_service):

    with pytest.raises(Exception):

        await database_service.sql.execute(
            """
            SELECT *
            FROM table_that_does_not_exist;
            """
        )