import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService

from gee.execution.execution_engine import ExecutionEngine

from gee.models.execution_command import Command
from gee.models.command_type import CommandType


@pytest.mark.asyncio
async def test_execution_engine_procedure(database_service):

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

    engine = ExecutionEngine(database_service)

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