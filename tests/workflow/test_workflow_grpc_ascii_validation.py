import io

import pytest
import pyarrow.ipc as ipc

from gee.grpc.generated import (
    execution_engine_pb2,
)


@pytest.mark.asyncio
async def test_workflow_grpc_ascii_validation(
    grpc_stub,
):
    """
    Workflow

        gRPC Procedure Execute
                  ↓
        Update word and sum
                  ↓
        gRPC SQL Query
                  ↓
        Arrow Stream
                  ↓
        Validate 100 Rows
    """

    #
    # Execute procedure through gRPC
    #
    procedure_request = (
        execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.PROCEDURE,
            command="execute_procedure",
        )
    )

    procedure_request.parameters.extend(
        [
            execution_engine_pb2.Parameter(
                name="schema",
                string_value="public",
            ),
            execution_engine_pb2.Parameter(
                name="procedure",
                string_value="calculate_ascii_metadata",
            ),
        ]
    )

    async def procedure_request_stream():

        yield procedure_request

    async for response in grpc_stub.Execute(
        procedure_request_stream()
    ):

        assert response.success is True

    #
    # Read data through gRPC
    #
    sql_request = (
        execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.SQL,
            command="""
            SELECT *
            FROM workflow_ascii
            ORDER BY random()
            LIMIT 100
            """,
        )
    )

    async def sql_request_stream():

        yield sql_request

    validated_rows = 0

    async for response in grpc_stub.Execute(
        sql_request_stream()
    ):

        assert response.success is True

        table = (
            ipc.open_stream(
                io.BytesIO(
                    response.payload
                )
            ).read_all()
        )

        data = table.to_pylist()

        for row in data:

            expected_word = (
                chr(row["ascii1"])
                + chr(row["ascii2"])
                + chr(row["ascii3"])
            )

            expected_sum = (
                row["ascii1"]
                + row["ascii2"]
                + row["ascii3"]
            )

            assert (
                row["word"]
                == expected_word
            )

            assert (
                row["sum"]
                == expected_sum
            )

            validated_rows += 1

    assert validated_rows == 100