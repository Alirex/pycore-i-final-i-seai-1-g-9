from typing import TYPE_CHECKING

import pytest

from persyval.services.data_storage.data_storage import DataStorage
from persyval.services.data_storage_filler.data_storage_filler import fill_data_storage

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture
def data_storage_fixture() -> Generator[DataStorage]:
    # https://docs.pytest.org/en/stable/how-to/fixtures.html#yield-fixtures-recommended
    with DataStorage.load(dir_path=None) as data_storage:
        yield data_storage


def test_data_storage_clear(
    data_storage_fixture: DataStorage,
) -> None:
    amount = 10

    fill_data_storage(
        data_storage=data_storage_fixture,
        amount=amount,
    )
    assert len(data_storage_fixture.data.contacts) == amount
    assert len(data_storage_fixture.data.notes) == 0

    data_storage_fixture.clear()
    assert len(data_storage_fixture.data.contacts) == 0
    assert len(data_storage_fixture.data.notes) == 0
