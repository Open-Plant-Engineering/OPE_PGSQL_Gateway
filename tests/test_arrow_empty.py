from gee.arrow.serializer import ArrowSerializer


def test_arrow_empty():

    payload = ArrowSerializer.serialize([])

    assert payload == b""