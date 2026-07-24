import pytest

from pydantic import ValidationError

from gee.config.streaming_settings import (
    StreamingSettings,
)


def test_streaming_settings_valid():

    settings = StreamingSettings(
        batch_size=1000,
    )

    assert settings.batch_size == 1000


def test_streaming_settings_rejects_zero():

    with pytest.raises(
        ValidationError
    ):

        StreamingSettings(
            batch_size=0,
        )


def test_streaming_settings_rejects_negative():

    with pytest.raises(
        ValidationError
    ):

        StreamingSettings(
            batch_size=-1,
        )