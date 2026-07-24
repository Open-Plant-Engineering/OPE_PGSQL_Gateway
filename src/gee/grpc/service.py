import logging
import time

from gee.config.settings import Settings

from gee.grpc.generated import (
    execution_engine_pb2,
    execution_engine_pb2_grpc,
)

from gee.execution.execution_engine import (
    ExecutionEngine,
)

from gee.models.execution_command import (
    Command,
)

from gee.models.command_type import (
    CommandType,
)

from gee.arrow.stream_serializer import (
    ArrowStreamSerializer,
)


logger = logging.getLogger(__name__)


class ExecutionEngineService(
    execution_engine_pb2_grpc.ExecutionEngineServicer,
):

    def __init__(
        self,
        execution_engine: ExecutionEngine,
        settings: Settings,
    ):
        self._execution_engine = (
            execution_engine
        )
        self._settings = settings

    async def Execute(
        self,
        request_iterator,
        context,
    ):

        async for request in request_iterator:

            if context.cancelled():
            
                logger.warning(
                    "Client cancelled request stream"
                )

                return

            start_time = (
                time.perf_counter()
            )

            try:
                self._validate_request(request)

                if (
                    request.type
                    == execution_engine_pb2.SQL
                ):

                    command_type = (
                        CommandType.SQL
                    )

                elif (
                    request.type
                    == execution_engine_pb2.FUNCTION
                ):

                    command_type = (
                        CommandType.FUNCTION
                    )

                elif (
                    request.type
                    == execution_engine_pb2.PROCEDURE
                ):

                    command_type = (
                        CommandType.PROCEDURE
                    )

                else:

                    raise ValueError(
                        "Unsupported command type: "
                        f"{request.type}"
                    )

                command_parameters = []

                for parameter in request.parameters:

                    value_field = (
                        parameter.WhichOneof(
                            "value"
                        )
                    )

                    if (
                        value_field
                        == "string_value"
                    ):

                        command_parameters.append(
                            parameter.string_value
                        )

                    elif (
                        value_field
                        == "int_value"
                    ):

                        command_parameters.append(
                            parameter.int_value
                        )

                    elif (
                        value_field
                        == "double_value"
                    ):

                        command_parameters.append(
                            parameter.double_value
                        )

                    elif (
                        value_field
                        == "bool_value"
                    ):

                        command_parameters.append(
                            parameter.bool_value
                        )

                    elif (
                        value_field
                        == "bytes_value"
                    ):

                        command_parameters.append(
                            parameter.bytes_value
                        )

                command = Command(
                    type=command_type,
                    command=request.command,
                    parameters=command_parameters,
                )

                #
                # Procedure Execution
                #
                if (
                    command.type
                    == CommandType.PROCEDURE
                ):

                    success = (
                        await self._execution_engine.execute(
                            command
                        )
                    )

                    yield (
                        execution_engine_pb2.CommandResponse(
                            success=success,
                            message="Success",
                            payload=b"",
                        )
                    )

                    elapsed_ms = (
                        time.perf_counter()
                        - start_time
                    ) * 1000

                    logger.info(
                        "Command=%s "
                        "Success=%s "
                        "TimeMs=%.2f",
                        command.type.name,
                        success,
                        elapsed_ms,
                    )

                    continue

                #
                # SQL / Function Streaming
                #
                batch_count = 0

                async for batch in (
                    self._execution_engine.stream(
                        command
                    )
                ):
                    if context.cancelled():
                    
                        logger.warning(
                            "Client cancelled request stream"
                        )

                        return
                    
                    batch_count += 1

                    payload = (
                        ArrowStreamSerializer.serialize_batch(
                            batch
                        )
                    )

                    yield (
                        execution_engine_pb2.CommandResponse(
                            success=True,
                            message="Success",
                            payload=payload,
                        )
                    )

                elapsed_ms = (
                    time.perf_counter()
                    - start_time
                ) * 1000

                logger.info(
                    "Command=%s "
                    "Success=%s "
                    "Batches=%s "
                    "TimeMs=%.2f",
                    command.type.name,
                    True,
                    batch_count,
                    elapsed_ms,
                )

            except Exception as ex:

                yield (
                    execution_engine_pb2.CommandResponse(
                        success=False,
                        message=str(ex),
                        payload=b"",
                    )
                )

                logger.exception(
                    "Command=%s Failed",
                    command_type.name
                    if "command_type" in locals()
                    else request.type,
                )

    def _validate_request(
        self,
        request,
    ):
        if not request.command.strip():

            raise ValueError(
                "Command cannot be empty"
            )

        parameter_names = {
            parameter.name
            for parameter in request.parameters
        }

        if (
            request.type
            == execution_engine_pb2.FUNCTION
        ):

            if "schema" not in parameter_names:

                raise ValueError(
                    "Missing function parameter: schema"
                )

            if "function" not in parameter_names:

                raise ValueError(
                    "Missing function parameter: function"
                )

        elif (
            request.type
            == execution_engine_pb2.PROCEDURE
        ):

            if "schema" not in parameter_names:

                raise ValueError(
                    "Missing procedure parameter: schema"
                )

            if "procedure" not in parameter_names:

                raise ValueError(
                    "Missing procedure parameter: procedure"
                )