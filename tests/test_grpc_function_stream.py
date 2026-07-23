import io

import pytest
import pyarrow.ipc as ipc

from gee.grpc.generated import (
    execution_engine_pb2,
)


@pytest.mark.asyncio
async def test_grpc_function_stream(
    database_service,
    grpc_stub,
):

    await database_service.sql.execute(
        """
        CREATE OR REPLACE FUNCTION public.generate_numbers(
            max_value integer
        )
        RETURNS TABLE(id integer)
        AS $$
        BEGIN
            RETURN QUERY
            SELECT *
            FROM generate_series(
                1,
                max_value
            );
        END;
        $$ LANGUAGE plpgsql;
        """
    )

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
                string_value="generate_numbers",
            ),
            execution_engine_pb2.Parameter(
                name="max_value",
                int_value=10000,
            ),
        ]
    )

    async def request_stream():

        yield request

    batch_count = 0

    total_rows = 0

    async for response in grpc_stub.Execute(
        request_stream()
    ):

        assert response.success is True

        batch_count += 1

        table = (
            ipc.open_stream(
                io.BytesIO(
                    response.payload
                )
            ).read_all()
        )

        total_rows += table.num_rows

    assert batch_count == 10

    assert total_rows == 10000