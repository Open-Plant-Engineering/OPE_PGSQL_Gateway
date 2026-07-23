from gee.grpc.generated import (
    execution_engine_pb2,
    execution_engine_pb2_grpc,
)

from gee.execution.execution_engine import ExecutionEngine

from gee.models.execution_command import Command
from gee.models.command_type import CommandType

from gee.arrow.stream_serializer import (
    ArrowStreamSerializer,
)


class ExecutionEngineService(
    execution_engine_pb2_grpc.ExecutionEngineServicer
):

    def __init__(
        self,
        execution_engine: ExecutionEngine,
    ):
        self._execution_engine = execution_engine

    async def Execute(
        self,
        request_iterator,
        context,
    ):
        async for request in request_iterator:
            if request.type == execution_engine_pb2.SQL:
                command_type = CommandType.SQL
    
            elif request.type == execution_engine_pb2.FUNCTION:
                command_type = CommandType.FUNCTION
    
            elif request.type == execution_engine_pb2.PROCEDURE:
                command_type = CommandType.PROCEDURE
    
            else:
            
                raise ValueError(
                    f"Unsupported command type: {request.type}"
                )
    
            command_parameters = []
    
            for parameter in request.parameters:
            
                value_field = parameter.WhichOneof(
                    "value"
                )
    
                if value_field == "string_value":
                    command_parameters.append(
                        parameter.string_value
                    )
    
                elif value_field == "int_value":
                    command_parameters.append(
                        parameter.int_value
                    )
    
                elif value_field == "double_value":
                    command_parameters.append(
                        parameter.double_value
                    )
    
                elif value_field == "bool_value":
                    command_parameters.append(
                        parameter.bool_value
                    )
    
                elif value_field == "bytes_value":
                    command_parameters.append(
                        parameter.bytes_value
                    )
    
            command = Command(
                type=command_type,
                command=request.command,
                parameters=command_parameters,
            )
    
            if command.type == CommandType.PROCEDURE:
            
                success = (
                    await self._execution_engine.execute(
                        command
                    )
                )
    
                yield execution_engine_pb2.CommandResponse(
                    success=success,
                    message="Success",
                    payload=b"",
                )
    
                return
    
            async for batch in (
                self._execution_engine.stream(
                    command
                )
            ):
    
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
