from gee.config.execution_settings import (
    ExecutionSettings,
)


def test_execution_timeout_default():

    settings = (
        ExecutionSettings()
    )

    assert (
        settings.timeout_seconds
        == 300
    )