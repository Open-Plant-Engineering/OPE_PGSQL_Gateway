import grpc
import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database import DatabaseService

from gee.grpc.generated import (
    execution_engine_pb2,
    execution_engine_pb2_grpc,
)


@pytest.mark.asyncio
async def test_workflow_grpc_procedure_execute():
    """
    Workflow:
        Client
          ↓
        gRPC
          ↓
        ExecutionEngine
          ↓
        Procedure Execution
          ↓
        PostgreSQL Procedure
          ↓
        Success Response
          ↓
        Client

    Scenario:
        Execute a PostgreSQL procedure through gRPC.

    Validation:
        - Procedure executes successfully
        - gRPC response is returned
        - Exactly one response is received

    Notes:
        - Procedures do not return a result set.
        - Procedures are executed using execute().
        - No Arrow serialization is involved.
        - No output streaming is involved.
        - V1 supports Procedure Execute only.
        - Procedure Stream Input is planned for future implementation.

    Workflow Type:
        Procedure Execute

    Streaming:
        gRPC Streaming API      ✅
        Procedure Input Stream  ❌
        Procedure Output Stream ❌

    Result:
        Single Procedure Execution
        Single Success Response

    """

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

    async with grpc.aio.insecure_channel(
        "localhost:50051"
    ) as channel:

        stub = (
            execution_engine_pb2_grpc.ExecutionEngineStub(
                channel
            )
        )

        request = execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.PROCEDURE,
            command="execute_procedure",
        )

        request.parameters.extend([
            execution_engine_pb2.Parameter(
                name="schema",
                string_value="public",
            ),
            execution_engine_pb2.Parameter(
                name="procedure",
                string_value="test_procedure",
            ),
            execution_engine_pb2.Parameter(
                name="message",
                string_value="Hello World",
            ),
        ])

        response_count = 0

        async for response in stub.Execute(request):

            assert response.success is True

            response_count += 1

        assert response_count == 1