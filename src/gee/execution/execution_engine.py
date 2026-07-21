from gee.models.command_type import CommandType


class ExecutionEngine:

    def __init__(self, database):
        self._database = database

    async def execute(self, command):

        if command.type == CommandType.SQL:
            return await self._database.sql.execute(
                command.command,
                *command.parameters,
            )

        if command.type == CommandType.FUNCTION:

            schema = command.parameters[0]
            function_name = command.parameters[1]

            params = command.parameters[2:]

            return await self._database.function.execute(
                schema,
                function_name,
                *params,
            )

        if command.type == CommandType.PROCEDURE:

            schema = command.parameters[0]
            procedure_name = command.parameters[1]

            params = command.parameters[2:]

            return await self._database.procedure.execute(
                schema,
                procedure_name,
                *params,
            )

        raise NotImplementedError(
            f"Unsupported command type: {command.type}"
        )

    async def stream(self, command):

        if command.type == CommandType.SQL:

            async for batch in self._database.sql.stream(
                command.command,
                *command.parameters,
            ):
                yield batch

        elif command.type == CommandType.FUNCTION:

            schema = command.parameters[0]
            function_name = command.parameters[1]

            params = command.parameters[2:]

            async for batch in self._database.function.stream(
                schema,
                function_name,
                *params,
            ):
                yield batch

        else:
            raise NotImplementedError(
                f"Streaming not implemented for {command.type}"
            )