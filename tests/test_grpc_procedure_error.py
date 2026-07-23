import pytest

from gee.grpc.generated import (
    execution_engine_pb2,
)


@pytest.mark.asyncio
async def test_grpc_procedure_error(
    grpc_stub,
):

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
                string_value="unknown_procedure",
            ),
        ]
    )

    async def request_stream():

        yield request

    responses = []

    async for response in grpc_stub.Execute(
        request_stream()
    ):

        responses.append(
            response
        )

    assert len(responses) == 1

    assert responses[0].success is False

    assert responses[0].message != ""