import enum
from typing import TYPE_CHECKING

from pydantic import BaseModel

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

    filter_field: str | None = None
    filter_value: str | None = None


def contact_list(
    data_storage: DataStorage,
    list_config: ContactsListConfig,
) -> list[Contact]:
    if list_config.filter_mode is not ListFilterModeEnum.ALL:
        raise NotImplementedError

    return list(data_storage.data.contacts.values())
