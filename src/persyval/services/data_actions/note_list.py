import enum
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from persyval.models.note import AllowedKeysToFilterForNote

if TYPE_CHECKING:
    from persyval.models.note import Note
    from persyval.services.data_storage.data_storage import DataStorage


@enum.unique
class ListFilterModeEnum(enum.StrEnum):
    ALL = enum.auto()
    FILTER = enum.auto()


class ListFilterModeMeta(BaseModel):
    mode: ListFilterModeEnum
    title: str


class NotesListConfig(BaseModel):
    filter_mode: ListFilterModeEnum
    queries_as_map: dict[
        AllowedKeysToFilterForNote,
        str,
    ] = Field(default_factory=dict)


LIST_FILTER_MODE_REGISTRY: dict[ListFilterModeEnum, ListFilterModeMeta] = {
    item.mode: item
    for item in [
        ListFilterModeMeta(
            mode=ListFilterModeEnum.ALL,
            title="Show all notes",
        ),
        ListFilterModeMeta(
            mode=ListFilterModeEnum.FILTER,
            title="Filter notes",
        ),
    ]
}


def extract_queries(
    list_config: NotesListConfig,
) -> tuple[str | None, str | None]:
    queries = dict(list_config.queries_as_map)

    title = queries.pop(AllowedKeysToFilterForNote.TITLE, None)
    content = queries.pop(AllowedKeysToFilterForNote.CONTENT, None)

    if title:
        title = title.lower()
    if content:
        content = content.lower()

    if queries:
        msg = f"Unknown queries. Keys: {', '.join(queries.keys())}"
        raise ValueError(msg)

    return title, content


def note_matches(
    note: Note,
    title: str | None,
    content: str | None,
) -> bool:
    if title:
        note_title = (note.title or "").lower()
        if title not in note_title:
            return False

    if content:
        note_content = (note.content or "").lower()
        if content not in note_content:
            return False

    return True


def note_list(
    data_storage: DataStorage,
    list_config: NotesListConfig,
) -> list[Note]:
    if list_config.filter_mode is ListFilterModeEnum.ALL:
        return list(data_storage.data.notes.values())

    title, content = extract_queries(list_config)

    return [note for note in data_storage.data.notes.values() if note_matches(note, title, content)]
