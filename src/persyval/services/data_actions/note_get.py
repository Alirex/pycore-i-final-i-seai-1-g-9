from typing import TYPE_CHECKING

from persyval.exceptions.main import NotFoundError
from persyval.models.note import Note

if TYPE_CHECKING:
    from persyval.models.note import NoteUid
    from persyval.services.data_storage.data_storage import DataStorage


def note_get(
    data_storage: DataStorage,
    uid: NoteUid,
) -> Note:
    try:
        return data_storage.data.notes[uid]
    except KeyError as exc:
        msg = f"{Note.get_meta_info().singular_name} with uid {uid} not found."
        raise NotFoundError(msg) from exc
