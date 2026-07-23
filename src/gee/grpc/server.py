import asyncio
import grpc

from gee.grpc.generated import (
    execution_engine_pb2_grpc,
)
from gee.config.settings import Settings

from gee.grpc.service import (
    ExecutionEngineService,
)

from gee.postgres.pool import PostgresPool
from gee.postgres.database_service import DatabaseService

from gee.execution.execution_engine import (
    ExecutionEngine,
)


async def serve():

    settings = Settings()

    pool = PostgresPool()

    await pool.connect(
        host=settings.pg_host,
        port=settings.pg_port,
        database=settings.pg_database,
        user=settings.pg_user,
        password=settings.pg_password,
    )

    db = DatabaseService(pool)

    engine = ExecutionEngine(db)

    server = grpc.aio.server()

    execution_engine_pb2_grpc.add_ExecutionEngineServicer_to_server(
        ExecutionEngineService(engine),
        server,
    )

    server.add_insecure_port(
        f"{settings.grpc_host}:{settings.grpc_port}"
    )

    await server.start()

    print(
        f"Server running on "
        f"{settings.grpc_host}:{settings.grpc_port}"
    )

    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())