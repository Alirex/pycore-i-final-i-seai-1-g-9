import enum
from typing import TYPE_CHECKING, Annotated

from pydantic import BaseModel, Field

from persyval.models.contact import parse_birthday

if TYPE_CHECKING:
    from persyval.models.contact import Contact
    from persyval.services.data_storage.data_storage import DataStorage


@enum.unique
class ListFilterModeEnum(enum.StrEnum):
    ALL = enum.auto()
    FILTER = enum.auto()


class ListFilterModeMeta(BaseModel):
    mode: ListFilterModeEnum
    title: str


LIST_FILTER_MODE_REGISTRY: dict[ListFilterModeEnum, ListFilterModeMeta] = {
    item.mode: item
    for item in [
        ListFilterModeMeta(
            mode=ListFilterModeEnum.ALL,
            title="Show all",
        ),
        ListFilterModeMeta(
            mode=ListFilterModeEnum.FILTER,
            title="Filter",
        ),
    ]
}

# TODO: Rework


class ContactsListConfig(BaseModel):
    filter_mode: ListFilterModeEnum

    queries_as_map: Annotated[dict[str, str], Field(default_factory=dict)]


# TODO: Refactor this function.


def contacts_list(  # noqa: C901, PLR0912
    data_storage: DataStorage,
    list_config: ContactsListConfig,
) -> list[Contact]:
    if list_config.filter_mode is ListFilterModeEnum.ALL:
        list(data_storage.data.contacts.values())

    queries_as_map = list_config.queries_as_map

    try:
        uid = queries_as_map.pop("uid")
    except KeyError:
        uid = None

    try:
        name = queries_as_map.pop("name")
    except KeyError:
        name = None

    try:
        address = queries_as_map.pop("address")
    except KeyError:
        address = None

    try:
        birthday_raw = queries_as_map.pop("birthday")
        birthday = parse_birthday(birthday_raw) if birthday_raw else None
    except KeyError:
        birthday = None

    try:
        phone = queries_as_map.pop("phones")
    except KeyError:
        phone = None

    try:
        email = queries_as_map.pop("emails")
    except KeyError:
        email = None

    if queries_as_map:
        msg = f"Unknown queries. Keys: {', '.join(queries_as_map.keys())}"
        raise ValueError(msg)

    result: list[Contact] = []
    for contact in data_storage.data.contacts.values():
        if uid and uid != contact.uid:
            continue

        if name and name not in contact.name:
            continue

        if address and contact.address and address not in contact.address:
            continue

        if birthday and contact.birthday and contact.birthday != birthday:
            continue

        if phone and not any(phone_item for phone_item in contact.phones if phone in phone_item):
            continue

        if email and not any(email_item for email_item in contact.emails if email in email_item):
            continue

        result.append(contact)

    return result
