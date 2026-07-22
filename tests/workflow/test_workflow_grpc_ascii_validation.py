import io

import grpc
import pytest
import pyarrow.ipc as ipc

from gee.grpc.generated import (
    execution_engine_pb2,
    execution_engine_pb2_grpc,
)


@pytest.mark.asyncio
async def test_workflow_grpc_ascii_validation():
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

    async with grpc.aio.insecure_channel(
        "localhost:50051"
    ) as channel:

        stub = (
            execution_engine_pb2_grpc.ExecutionEngineStub(
                channel
            )
        )

        #
        # Execute procedure through gRPC
        #
        procedure_request = (
            execution_engine_pb2.CommandRequest(
                type=execution_engine_pb2.PROCEDURE,
                command="execute_procedure",
            )
        )

        procedure_request.parameters.extend([
            execution_engine_pb2.Parameter(
                name="schema",
                string_value="public",
            ),
            execution_engine_pb2.Parameter(
                name="procedure",
                string_value="calculate_ascii_metadata",
            ),
        ])

        async for response in stub.Execute(
            procedure_request
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

        validated_rows = 0

        async for response in stub.Execute(
            sql_request
        ):

            assert response.success is True

            table = (
                ipc.open_stream(
                    io.BytesIO(response.payload)
                ).read_all()
            )

            data = table.to_pylist()

            for row in data:

                expected_word = (
                    chr(row["ascii1"]) +
                    chr(row["ascii2"]) +
                    chr(row["ascii3"])
                )

                expected_sum = (
                    row["ascii1"] +
                    row["ascii2"] +
                    row["ascii3"]
                )

                assert row["word"] == expected_word
                assert row["sum"] == expected_sum

                validated_rows += 1

        assert validated_rows == 100