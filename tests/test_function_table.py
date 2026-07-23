import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService


@pytest.mark.asyncio
async def test_get_numbers(database_service):

    await database_service.sql.execute(
        """
        CREATE OR REPLACE FUNCTION public.get_numbers()
        RETURNS TABLE(
            id integer,
            value text
        )
        AS $$
        BEGIN
            RETURN QUERY
            SELECT 1, 'One'
            UNION ALL
            SELECT 2, 'Two'
            UNION ALL
            SELECT 3, 'Three';
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    rows = await database_service.function.execute(
        "public",
        "get_numbers"
    )

    assert len(rows) == 3

    assert rows[0]["id"] == 1
    assert rows[0]["value"] == "One"

    assert rows[1]["id"] == 2
    assert rows[1]["value"] == "Two"

    assert rows[2]["id"] == 3
    assert rows[2]["value"] == "Three"