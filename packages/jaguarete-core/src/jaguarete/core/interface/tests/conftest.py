import pytest

from jaguarete.core.interface.storage import InMemoryStorage
from jaguarete.util.serialization.json_serialization import JsonSerializer


@pytest.fixture
def serializer():
    return JsonSerializer()


@pytest.fixture
def in_memory_storage(serializer):
    return InMemoryStorage(serializer)
