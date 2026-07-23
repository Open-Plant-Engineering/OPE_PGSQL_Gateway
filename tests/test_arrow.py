import pytest

from gee.arrow.serializer import (
    ArrowSerializer,
)

from gee.arrow.deserializer import (
    ArrowDeserializer,
)


@pytest.mark.asyncio
async def test_arrow_roundtrip(
    database_service,
):

    await database_service.sql.execute(
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

    rows = await (
        database_service.function.execute(
            "public",
            "get_numbers",
        )
    )

    payload = (
        ArrowSerializer.serialize(
            rows
        )
    )

    assert payload is not None
    assert len(payload) > 0

    table = (
        ArrowDeserializer.deserialize(
            payload
        )
    )

    assert table.num_rows == 3

    data = table.to_pydict()

    assert data["id"] == [1, 2, 3]

    assert data["value"] == [
        "One",
        "Two",
        "Three",
    ]