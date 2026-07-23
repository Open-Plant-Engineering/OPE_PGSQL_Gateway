import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService


@pytest.mark.asyncio
async def test_procedure_execute(database_service):

    await database_service.sql.execute(
        """
        CREATE OR REPLACE PROCEDURE public.test_procedure(
            msg text
        )
        LANGUAGE plpgsql
        AS $$
        BEGIN
            RAISE NOTICE 'Message: %', msg;
        END;
        $$;
        """
    )

    result = await database_service.procedure.execute(
        "public",
        "test_procedure",
        "Hello World",
    )

    assert result is True