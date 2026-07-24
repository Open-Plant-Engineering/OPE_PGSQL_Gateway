import pytest

from gee.grpc.generated import (
    execution_engine_pb2,
)


@pytest.mark.asyncio
async def test_empty_command(
    grpc_stub,
):

    request = (
        execution_engine_pb2.CommandRequest(
            type=execution_engine_pb2.SQL,
            command="",
        )
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

    assert (
        "Command cannot be empty"
        in responses[0].message
    )

import pytest

from gee.grpc.generated import (
    execution_engine_pb2,
)


@pytest.mark.asyncio
async def test_missing_function_parameter(
    grpc_stub,
):

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

    assert (
        "Missing function parameter: function"
        in responses[0].message
    )