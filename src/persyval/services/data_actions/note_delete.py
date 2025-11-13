from typing import TYPE_CHECKING

from persyval.exceptions.main import NotFoundError

if TYPE_CHECKING:
    from persyval.models.note import NoteUid
    from persyval.services.data_storage.data_storage import DataStorage


def note_delete(
    data_storage: DataStorage,
    note_uid: NoteUid,
) -> None:
    try:
        with data_storage.autosave():
            del data_storage.data.notes[note_uid]
    except KeyError as exc:
        msg = f"Note with uid {note_uid} not found."
        raise NotFoundError(msg) from exc
