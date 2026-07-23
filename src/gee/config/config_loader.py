import os
import tomllib
from pathlib import Path
from gee.config.settings import Settings


class ConfigLoader:

    @classmethod
    def load(
        cls,
        profile_name: str,
    ) -> Settings:
        
        DEFAULT_CONFIG_PATH = (
                Path(__file__).parent / "gee.toml"
        )

        config_path = os.getenv(
            "GEE_CONFIG",
            DEFAULT_CONFIG_PATH
        )

        with open(
            config_path,
            "rb",
        ) as file:

            config = tomllib.load(
                file
            )

        profiles = config.get(
            "profiles",
            {}
        )

        if (
            profile_name
            not in profiles
        ):
            raise ValueError(
                f"Profile not found: "
                f"{profile_name}"
            )

        profile = profiles[
            profile_name
        ]

        return Settings(
            profile_name=profile_name,
            postgres=profile[
                "postgres"
            ],
            grpc=profile[
                "grpc"
            ],
            streaming=profile[
                "streaming"
            ]
        )