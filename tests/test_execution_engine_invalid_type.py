import pytest

from gee.execution.execution_engine import ExecutionEngine


class DummyCommand:
    type = "INVALID"
    command = ""
    parameters = []


@pytest.mark.asyncio
async def test_execution_engine_invalid_type():

    engine = ExecutionEngine(None)

    with pytest.raises(
        NotImplementedError
    ):
        await engine.execute(
            DummyCommand()
        )