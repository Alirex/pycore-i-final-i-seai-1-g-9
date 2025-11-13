import pathlib
from typing import TYPE_CHECKING, Self

from pydantic import BaseModel, Field

from persyval.models.contact import Contact, ContactUid
from persyval.models.note import Note, NoteUid

if TYPE_CHECKING:
    from types import TracebackType


# Note: Use `thin model` when available. So, all methods created as separated functions.


class Data(BaseModel):
    contacts: dict[ContactUid, Contact] = Field(
        default_factory=dict,
        description="Dictionary of contacts indexed by their unique identifiers.",
    )

    notes: dict[NoteUid, Note] = Field(
        default_factory=dict,
        description="Dictionary of notes indexed by their unique identifiers.",
    )

    def clear(self) -> None:
        self.contacts.clear()
        self.notes.clear()


class DataStorage(BaseModel):
    path: pathlib.Path

    data: Data

    @classmethod
    def load(
        cls,
        dir_path: pathlib.Path,
    ) -> Self:
        path = dir_path / "data.json"

        try:
            with path.open("r", encoding="utf-8") as file:
                data = Data.model_validate_json(file.read())
        except FileNotFoundError:
            data = Data()

        return cls(path=path, data=data)

    def save(self) -> None:
        dir_path = self.path.parent
        dir_path.mkdir(parents=True, exist_ok=True)

        with self.path.open("w", encoding="utf-8") as file:
            file.write(self.data.model_dump_json(indent=4, ensure_ascii=False))

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        self.save()
        return None

    def clear(self) -> None:
        self.data.clear()
