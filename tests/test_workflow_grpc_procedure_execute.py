import pytest

from gee.grpc.generated import (
    execution_engine_pb2,
)


@pytest.mark.asyncio
async def test_workflow_grpc_procedure_execute(
    database_service,
    grpc_stub,
):
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

    request = (
        execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.PROCEDURE,
            command="execute_procedure",
        )
    )

    request.parameters.extend(
        [
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
        ]
    )

    async def request_stream():

        yield request

    response_count = 0

    async for response in grpc_stub.Execute(
        request_stream()
    ):

        assert response.success is True

        response_count += 1

    assert response_count == 1