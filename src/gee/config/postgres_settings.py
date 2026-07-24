from pydantic import BaseModel
from pydantic import Field
from pydantic import model_validator


class PostgresSettings(BaseModel):

    host: str

    port: int = Field(
        gt=0,
    )

    database: str

    user: str

    password: str

    min_pool_size: int = Field(
        default=5,
        gt=0,
    )

    max_pool_size: int = Field(
        default=20,
        gt=0,
    )

    @model_validator(
        mode="after"
    )
    def validate_pool_sizes(self):

        if (
            self.max_pool_size
            < self.min_pool_size
        ):
            raise ValueError(
                "max_pool_size must be "
                "greater than or equal to "
                "min_pool_size"
            )

        return self