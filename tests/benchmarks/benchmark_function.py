import asyncio
import time

import grpc

from gee.grpc.generated import (
    execution_engine_pb2,
    execution_engine_pb2_grpc,
)


TOTAL_REQUESTS = 1000


async def request_stream():

    for _ in range(
        TOTAL_REQUESTS
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
                execution_engine_pb2.Parameter(
                    name="function",
                    string_value="add_numbers",
                ),
                execution_engine_pb2.Parameter(
                    name="a",
                    int_value=10,
                ),
                execution_engine_pb2.Parameter(
                    name="b",
                    int_value=20,
                ),
            ]
        )

        yield request


async def main():

    async with grpc.aio.insecure_channel(
        "localhost:50051"
    ) as channel:

        stub = (
            execution_engine_pb2_grpc.ExecutionEngineStub(
                channel
            )
        )

        responses = 0

        start = time.perf_counter()

        async for response in stub.Execute(
            request_stream()
        ):

            if response.success:

                responses += 1

        elapsed = (
            time.perf_counter()
            - start
        )

        print(
            f"Requests     : {responses}"
        )

        print(
            f"Elapsed Sec  : {elapsed:.2f}"
        )

        print(
            f"Requests/Sec : "
            f"{responses / elapsed:.2f}"
        )


if __name__ == "__main__":

    asyncio.run(
        main()
    )
