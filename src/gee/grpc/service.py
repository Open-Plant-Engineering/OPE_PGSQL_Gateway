import asyncio
import grpc

from gee.grpc.generated import (
    execution_engine_pb2,
    execution_engine_pb2_grpc,
)

from gee.execution.execution_engine import ExecutionEngine
from gee.models.command import Command
from gee.models.command_type import CommandType
from gee.arrow.stream_serializer import (
    ArrowStreamSerializer,
)

class ExecutionEngineService(
    execution_engine_pb2_grpc.ExecutionEngineServicer
):
    def __init__(self, engine: ExecutionEngine):
        self._engine = engine

    async def Execute(
        self,
        request,
        context,
    ):
        if request.type == execution_engine_pb2.SQL:
            cmd_type = CommandType.SQL

        elif request.type == execution_engine_pb2.FUNCTION:
            cmd_type = CommandType.FUNCTION

        elif request.type == execution_engine_pb2.PROCEDURE:
            cmd_type = CommandType.PROCEDURE

        else:
            raise ValueError(
                f"Unsupported command type: {request.type}"
            )

        command = Command(
            type=cmd_type,
            command=request.command,
            parameters=[],
        )


        async for batch in self._engine.stream(command):
        
            payload = (
                ArrowStreamSerializer.serialize_batch(
                    batch
                )
            )

            yield execution_engine_pb2.CommandResponse(
                success=True,
                message="Success",
                payload=payload,
            )