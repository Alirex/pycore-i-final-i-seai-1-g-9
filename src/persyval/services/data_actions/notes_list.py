from typing import TYPE_CHECKING

from persyval.models.note import Note
from persyval.services.handlers.shared.sort_and_filter import ListConfig, filter_iterable

if TYPE_CHECKING:
    from persyval.services.data_storage.data_storage import DataStorage

NotesListConfig = ListConfig


def note_list(
    data_storage: DataStorage,
    list_config: NotesListConfig,
) -> list[Note]:
    return filter_iterable(
        iterable=data_storage.data.contacts.values(),
        model=Note,
        list_config=list_config,
    )
