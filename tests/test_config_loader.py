from gee.config.config_loader import (
    ConfigLoader,
)


def test_config_loader():

    settings = (
        ConfigLoader.load(
            "ope"
        )
    )

    assert (
        settings.profile_name
        == "ope"
    )

    assert (
        settings.streaming.batch_size
        > 0
    )

    assert (
        settings.postgres.port
        > 0
    )

    assert (
        settings.grpc.port
        > 0
    )