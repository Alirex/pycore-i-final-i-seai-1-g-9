from typing import TYPE_CHECKING

import pytest

from persyval.exceptions.main import AlreadyExistsError, NotFoundError
from persyval.models.contact import Contact
from persyval.services.data_actions.contact_add import contact_add
from persyval.services.data_actions.contact_delete import contact_delete
from persyval.services.data_actions.contact_get import contact_get
from persyval.services.data_storage.data_storage import DataStorage

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture
def data_storage_fixture() -> Generator[DataStorage]:
    # https://docs.pytest.org/en/stable/how-to/fixtures.html#yield-fixtures-recommended
    with DataStorage.load(dir_path=None) as data_storage:
        yield data_storage


@pytest.fixture(scope="module")
def data_storage_long_fixture() -> Generator[DataStorage]:
    # https://docs.pytest.org/en/stable/how-to/fixtures.html#yield-fixtures-recommended
    with DataStorage.load(dir_path=None) as data_storage:
        yield data_storage


@pytest.mark.parametrize(
    "contact",
    [
        Contact(
            name="Test",
        ),
    ],
)
def test_contact_i_add_i_get_i_remove(
    contact: Contact,
    data_storage_fixture: DataStorage,
) -> None:
    contact_add(
        data_storage=data_storage_fixture,
        contact=contact,
    )

    retrieved_contact = contact_get(
        data_storage=data_storage_fixture,
        contact_uid=contact.uid,
    )

    assert contact == retrieved_contact

    try:
        contact_add(
            data_storage=data_storage_fixture,
            contact=contact,
        )
    except AlreadyExistsError:
        pass
    else:
        pytest.fail("Expected AlreadyExistsError")

    contact_delete(
        data_storage=data_storage_fixture,
        contact_uid=contact.uid,
    )

    try:
        contact_delete(
            data_storage=data_storage_fixture,
            contact_uid=contact.uid,
        )
    except NotFoundError:
        pass
    else:
        pytest.fail("Expected NotFoundError")
