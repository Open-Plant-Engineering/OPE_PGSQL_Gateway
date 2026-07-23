import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService


@pytest.mark.asyncio
async def test_postgresql_connection(database_service):

    rows = await database_service.sql.execute(
        "select version();"
    )

    assert len(rows) == 1

    version = rows[0]["version"]

    assert version is not None
    assert "PostgreSQL" in version