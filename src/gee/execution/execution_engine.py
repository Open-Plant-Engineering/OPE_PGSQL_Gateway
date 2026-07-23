from gee.models.command_type import CommandType


class ExecutionEngine:

    def __init__(
        self,
        database_service,
    ):
        self._database_service = (
            database_service
        )

    async def execute(
        self,
        command,
    ):

        if command.type == CommandType.SQL:

            return await (
                self._database_service.sql.execute(
                    command.command,
                    *command.parameters,
                )
            )

        if command.type == CommandType.FUNCTION:

            schema_name = command.parameters[0]

            function_name = (
                command.parameters[1]
            )

            function_parameters = (
                command.parameters[2:]
            )

            return await (
                self._database_service.function.execute(
                    schema_name,
                    function_name,
                    *function_parameters,
                )
            )

        if command.type == CommandType.PROCEDURE:

            schema_name = command.parameters[0]

            procedure_name = (
                command.parameters[1]
            )

            procedure_parameters = (
                command.parameters[2:]
            )

            return await (
                self._database_service.procedure.execute(
                    schema_name,
                    procedure_name,
                    *procedure_parameters,
                )
            )

        raise NotImplementedError(
            f"Unsupported command type: {command.type}"
        )

    async def stream(
        self,
        command,
    ):

        if command.type == CommandType.SQL:

            async for batch in (
                self._database_service.sql.stream(
                    command.command,
                    *command.parameters,
                )
            ):
                yield batch

            return

        if command.type == CommandType.FUNCTION:

            schema_name = command.parameters[0]

            function_name = (
                command.parameters[1]
            )

            function_parameters = (
                command.parameters[2:]
            )

            async for batch in (
                self._database_service.function.stream(
                    schema_name,
                    function_name,
                    *function_parameters,
                )
            ):
                yield batch

            return

        raise NotImplementedError(
            f"Streaming not implemented for {command.type}"
        )