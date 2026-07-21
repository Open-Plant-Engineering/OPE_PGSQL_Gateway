import asyncio
import grpc
import io
import pyarrow.ipc as ipc

from gee.grpc.generated import (
    execution_engine_pb2,
    execution_engine_pb2_grpc,
)


async def main():

    async with grpc.aio.insecure_channel(
        "localhost:50051"
    ) as channel:

        stub = (
            execution_engine_pb2_grpc.ExecutionEngineStub(
                channel
            )
        )

        request = execution_engine_pb2.CommandRequest(
            request_id="1",
            type=execution_engine_pb2.FUNCTION,
            command="execute_function",
        )

        request.parameters.extend([
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
        ])

        response_stream = stub.Execute(request)

        batch_no = 0
        total_rows = 0

        async for response in response_stream:

            batch_no += 1

            table = (
                ipc.open_stream(
                    io.BytesIO(response.payload)
                ).read_all()
            )

            total_rows += table.num_rows

            print(
                f"Batch {batch_no}: "
                f"{table.num_rows} rows"
            )

        print(
            f"Total Rows: {total_rows}"
        )


if __name__ == "__main__":
    asyncio.run(main())