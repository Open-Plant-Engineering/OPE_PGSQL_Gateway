import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService


@pytest.mark.asyncio
async def test_add_numbers(database_service):

    await database_service.sql.execute(
        """
        CREATE OR REPLACE FUNCTION public.add_numbers(
            a integer,
            b integer
        )
        RETURNS integer
        AS $$
        BEGIN
            RETURN a + b;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    rows = await database_service.function.execute(
        "public",
        "add_numbers",
        10,
        20,
    )

    assert len(rows) == 1
    assert rows[0]["add_numbers"] == 30