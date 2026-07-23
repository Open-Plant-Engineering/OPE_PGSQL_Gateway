import io

import pytest
import pyarrow.ipc as ipc

from gee.grpc.generated import (
    execution_engine_pb2,
)


@pytest.mark.asyncio
async def test_workflow_grpc_ascii_function_update(
    grpc_stub,
):
    """
    Workflow

        gRPC Function
              ↓
        Update Row
              ↓
        gRPC SQL
              ↓
        Validate Updated Values
    """

    #
    # Update row #1 to XYZ
    #
    request = (
        execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.FUNCTION,
            command="execute_function",
        )
    )

    request.parameters.extend(
        [
            execution_engine_pb2.Parameter(
                name="schema",
                string_value="public",
            ),
            execution_engine_pb2.Parameter(
                name="function",
                string_value="update_ascii_row",
            ),
            execution_engine_pb2.Parameter(
                name="id",
                int_value=1,
            ),
            execution_engine_pb2.Parameter(
                name="ascii1",
                int_value=88,  # X
            ),
            execution_engine_pb2.Parameter(
                name="ascii2",
                int_value=89,  # Y
            ),
            execution_engine_pb2.Parameter(
                name="ascii3",
                int_value=90,  # Z
            ),
        ]
    )

    async def update_request_stream():

        yield request

    async for response in grpc_stub.Execute(
        update_request_stream()
    ):

        assert response.success is True

    #
    # Read row back
    #
    sql_request = (
        execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.SQL,
            command="""
            SELECT
                id,
                ascii1,
                ascii2,
                ascii3
            FROM workflow_ascii
            WHERE id = 1
            """,
        )
    )

    async def sql_request_stream():

        yield sql_request

    rows_found = 0

    async for response in grpc_stub.Execute(
        sql_request_stream()
    ):

        table = (
            ipc.open_stream(
                io.BytesIO(
                    response.payload
                )
            ).read_all()
        )

        data = table.to_pylist()

        assert len(data) == 1

        row = data[0]

        assert row["ascii1"] == 88
        assert row["ascii2"] == 89
        assert row["ascii3"] == 90

        rows_found += 1

    assert rows_found == 1