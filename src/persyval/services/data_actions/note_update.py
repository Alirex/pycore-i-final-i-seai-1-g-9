from typing import TYPE_CHECKING

from persyval.exceptions.main import NotFoundError
from persyval.models.note import Note

if TYPE_CHECKING:
    from persyval.models.note import NoteUid
    from persyval.services.data_storage.data_storage import DataStorage


def note_update(
    data_storage: DataStorage,
    note_uid: NoteUid,
    #
    new_title: str,
    new_content: str,
    new_tags: list[str],
) -> None:
    try:
        target_note = data_storage.data.notes[note_uid]
        target_note.title = new_title
        target_note.content = new_content
        target_note.tags = new_tags

    except KeyError as exc:
        msg = f"{Note.get_meta_info().singular_name} with uid {note_uid} not found."
        raise NotFoundError(msg) from exc
