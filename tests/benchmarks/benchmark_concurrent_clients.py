import asyncio
import time

import grpc

from gee.grpc.generated import (
    execution_engine_pb2,
    execution_engine_pb2_grpc,
)


CLIENT_COUNT = 50

REQUESTS_PER_CLIENT = 100


async def run_client():

    async with grpc.aio.insecure_channel(
        "localhost:50051"
    ) as channel:

        stub = (
            execution_engine_pb2_grpc.ExecutionEngineStub(
                channel
            )
        )

        async def request_stream():

            for _ in range(
                REQUESTS_PER_CLIENT
            ):

                yield (
                    execution_engine_pb2.CommandRequest(
                        type=execution_engine_pb2.SQL,
                        command="""
                        SELECT 1 AS id
                        """,
                    )
                )

        responses = 0

        async for response in stub.Execute(
            request_stream()
        ):

            if response.success:

                responses += 1

        return responses


async def main():

    total_requests = (
        CLIENT_COUNT
        * REQUESTS_PER_CLIENT
    )

    start = time.perf_counter()

    results = await asyncio.gather(
        *[
            run_client()
            for _ in range(
                CLIENT_COUNT
            )
        ]
    )

    elapsed = (
        time.perf_counter()
        - start
    )

    total_responses = sum(
        results
    )

    print(
        f"Clients              : "
        f"{CLIENT_COUNT}"
    )

    print(
        f"Requests Per Client  : "
        f"{REQUESTS_PER_CLIENT}"
    )

    print(
        f"Total Requests       : "
        f"{total_requests}"
    )

    print(
        f"Total Responses      : "
        f"{total_responses}"
    )

    print(
        f"Elapsed Sec          : "
        f"{elapsed:.2f}"
    )

    print(
        f"Requests/Sec         : "
        f"{total_responses / elapsed:.2f}"
    )


if __name__ == "__main__":

    asyncio.run(
        main()
    )