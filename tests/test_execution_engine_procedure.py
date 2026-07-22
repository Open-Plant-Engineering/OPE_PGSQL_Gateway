import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database import DatabaseService

from gee.execution.execution_engine import ExecutionEngine

from gee.models.command import Command
from gee.models.command_type import CommandType


@pytest.mark.asyncio
async def test_execution_engine_procedure():

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

    engine = ExecutionEngine(db)

    command = Command(
        type=CommandType.PROCEDURE,
        command="execute_procedure",
        parameters=[
            "public",
            "test_procedure",
            "Hello World",
        ],
    )

    result = await engine.execute(command)

    assert result is True