import copy
from typing import TYPE_CHECKING

import pytest

from persyval.exceptions.main import AlreadyExistsError, NotFoundError
from persyval.models.contact import Contact
from persyval.services.data_actions.contact_add import contact_add
from persyval.services.data_actions.contact_delete import contact_delete
from persyval.services.data_actions.contact_get import contact_get
from persyval.services.data_actions.contact_update import contact_update
from persyval.services.data_actions.contacts_list import ContactsListConfig, contacts_list
from persyval.services.data_storage.data_storage import DataStorage
from persyval.services.handlers.shared.sort_and_filter import ListFilterModeEnum

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
    contact_uid = contact.uid

    contacts_amount_before = len(
        contacts_list(
            data_storage=data_storage_fixture,
            list_config=ContactsListConfig(
                filter_mode=ListFilterModeEnum.ALL,
            ),
        ),
    )
    assert contacts_amount_before == 0

    contact_add(
        data_storage=data_storage_fixture,
        contact=contact,
    )

    retrieved_contact = contact_get(
        data_storage=data_storage_fixture,
        uid=contact_uid,
    )

    assert contact == retrieved_contact

    contact_copy = copy.deepcopy(contact)
    name = "Test 2"
    contact_copy.name = name

    contact_update(
        data_storage=data_storage_fixture,
        contact=contact_copy,
    )

    retrieved_contact_updated = contact_get(
        data_storage=data_storage_fixture,
        uid=contact_uid,
    )

    assert retrieved_contact_updated.name == name

    contacts_amount_after_add_all = len(
        contacts_list(
            data_storage=data_storage_fixture,
            list_config=ContactsListConfig(
                filter_mode=ListFilterModeEnum.ALL,
            ),
        ),
    )
    amount_after_add_expected = contacts_amount_before + 1
    assert contacts_amount_after_add_all == amount_after_add_expected

    contacts_amount_after_add_filtered = len(
        contacts_list(
            data_storage=data_storage_fixture,
            list_config=ContactsListConfig(
                filter_mode=ListFilterModeEnum.FILTER,
                filter_query={"name": name},
            ),
        ),
    )
    assert contacts_amount_after_add_filtered == 1

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
        contact_uid=contact_uid,
    )

    try:
        contact_delete(
            data_storage=data_storage_fixture,
            contact_uid=contact_uid,
        )
    except NotFoundError:
        pass
    else:
        pytest.fail("Expected NotFoundError")

    try:
        contact_get(
            data_storage=data_storage_fixture,
            uid=contact_uid,
        )
    except NotFoundError:
        pass
    else:
        pytest.fail("Expected NotFoundError")

    contacts_amount_end = len(
        contacts_list(
            data_storage=data_storage_fixture,
            list_config=ContactsListConfig(
                filter_mode=ListFilterModeEnum.ALL,
            ),
        ),
    )
    assert contacts_amount_end == contacts_amount_after_add_all - 1
