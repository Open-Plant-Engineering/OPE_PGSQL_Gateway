import asyncio

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database import DatabaseService

from gee.execution.execution_engine import ExecutionEngine

from gee.models.command import Command
from gee.models.command_type import CommandType


async def main():

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

    command = Command(
        type=CommandType.SQL,
        command="select * from generate_series(1,5) as id",
        parameters=[]
    )

    rows = await engine.execute(command)

    for row in rows:
        print(dict(row))


asyncio.run(main())