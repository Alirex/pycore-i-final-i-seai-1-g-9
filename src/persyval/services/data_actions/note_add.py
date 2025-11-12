from typing import TYPE_CHECKING

from persyval.exceptions.main import AlreadyExistsError

if TYPE_CHECKING:
    from persyval.models.note import Note
    from persyval.services.data_storage.data_storage import DataStorage


def note_add(
    data_storage: DataStorage,
    note: Note,
) -> Note:
    if note.uid in data_storage.data.notes:
        msg = f"Note with uid {note.uid} already exists."
        raise AlreadyExistsError(msg)

    data_storage.data.notes[note.uid] = note

    return note
