import asyncio
import sys
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

from gee.config.config_loader import (
    ConfigLoader,
)

async def serve():

    profile_name = sys.argv[1]
    
    settings = ConfigLoader.load(profile_name)

    pool = PostgresPool(settings)

    await pool.connect()

    db = DatabaseService(pool)

    engine = ExecutionEngine(db)

    server = grpc.aio.server()

    execution_engine_pb2_grpc.add_ExecutionEngineServicer_to_server(
        ExecutionEngineService(engine),
        server,
    )

    server.add_insecure_port(
        f"{settings.grpc.host}:{settings.grpc.port}"
    )

    await server.start()

    print(
        f"Server running on "
        f"{settings.grpc.host}:{settings.grpc.port}"
    )

    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())