from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from persyval.models.note import Note
    from persyval.services.data_storage.data_storage import DataStorage


def note_list(data_storage: DataStorage) -> list[Note]:
    notes_list = list(data_storage.data.notes.values())

    notes_list.sort(key=lambda note: note.uid)

    return notes_list
