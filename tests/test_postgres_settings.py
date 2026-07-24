import pytest

from pydantic import ValidationError

from gee.config.postgres_settings import (
    PostgresSettings,
)


def create_settings(
    min_pool_size=5,
    max_pool_size=20,
):

    return PostgresSettings(
        host="localhost",
        port=5432,
        database="test",
        user="postgres",
        password="postgres",
        min_pool_size=min_pool_size,
        max_pool_size=max_pool_size,
    )


def test_postgres_settings_valid():

    settings = create_settings()

    assert settings.port == 5432


def test_postgres_settings_rejects_zero_port():

    with pytest.raises(
        ValidationError
    ):

        PostgresSettings(
            host="localhost",
            port=0,
            database="test",
            user="postgres",
            password="postgres",
            min_pool_size=5,
            max_pool_size=20,
        )


def test_postgres_settings_rejects_zero_min_pool():

    with pytest.raises(
        ValidationError
    ):

        create_settings(
            min_pool_size=0,
        )


def test_postgres_settings_rejects_zero_max_pool():

    with pytest.raises(
        ValidationError
    ):

        create_settings(
            max_pool_size=0,
        )


def test_postgres_settings_rejects_invalid_pool_range():

    with pytest.raises(
        ValidationError
    ):

        create_settings(
            min_pool_size=20,
            max_pool_size=5,
        )