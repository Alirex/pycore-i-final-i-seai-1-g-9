from typing import TYPE_CHECKING

from persyval.models.contact import Contact
from persyval.services.handlers.shared.sort_and_filter import ListConfig, filter_iterable

if TYPE_CHECKING:
    from persyval.services.data_storage.data_storage import DataStorage


# TODO: Rework


# TODO: Refactor this function.


def contacts_list(
    data_storage: DataStorage,
    list_config: ListConfig,
) -> list[Contact]:
    return filter_iterable(
        iterable=data_storage.data.contacts.values(),
        model=Contact,
        list_config=list_config,
    )
