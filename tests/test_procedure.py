import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService


@pytest.mark.asyncio
async def test_procedure_execute():

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

    await db.sql.execute(
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

    result = await db.procedure.execute(
        "public",
        "test_procedure",
        "Hello World",
    )

    assert result is True