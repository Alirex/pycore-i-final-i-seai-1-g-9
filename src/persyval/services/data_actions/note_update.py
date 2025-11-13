from typing import TYPE_CHECKING

from persyval.exceptions.main import NotFoundError

if TYPE_CHECKING:
    from persyval.models.note import NoteUid
    from persyval.services.data_storage.data_storage import DataStorage


def note_update(
    data_storage: DataStorage,
    note_uid: NoteUid,
    new_title: str,
    new_content: str,
) -> None:
    try:
        target_note = data_storage.data.notes[note_uid]
        target_note.title = new_title
        target_note.content = new_content

    except KeyError as exc:
        msg = f"Note with uid {note_uid} not found."
        raise NotFoundError(msg) from exc
