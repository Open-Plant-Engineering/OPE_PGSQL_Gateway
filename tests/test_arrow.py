import pytest

from gee.config.settings import Settings
from gee.postgres.pool import PostgresPool
from gee.postgres.database import DatabaseService

from gee.arrow.serializer import ArrowSerializer
from gee.arrow.deserializer import ArrowDeserializer


@pytest.mark.asyncio
async def test_arrow_roundtrip():

    settings = Settings()

    pool = PostgresPool()

    await pool.connect(
        host=settings.pg_host,
        port=settings.pg_port,
        database=settings.pg_database,
        user=settings.pg_user,
        password=settings.pg_password,
    )

    db = DatabaseService(pool)

    await db.sql.execute(
        """
        CREATE OR REPLACE FUNCTION public.get_numbers()
        RETURNS TABLE(
            id integer,
            value text
        )
        AS $$
        BEGIN
            RETURN QUERY
            SELECT 1, 'One'
            UNION ALL
            SELECT 2, 'Two'
            UNION ALL
            SELECT 3, 'Three';
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    rows = await db.function.execute(
        "public",
        "get_numbers"
    )

    payload = ArrowSerializer.serialize(rows)

    assert payload is not None
    assert len(payload) > 0

    table = ArrowDeserializer.deserialize(payload)

    assert table.num_rows == 3

    data = table.to_pydict()

    assert data["id"] == [1, 2, 3]
    assert data["value"] == ["One", "Two", "Three"]