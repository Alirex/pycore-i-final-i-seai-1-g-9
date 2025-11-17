import pathlib
from typing import TYPE_CHECKING, Annotated, Self

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


class DataStorageAutosaver(BaseModel):
    data_storage: DataStorage

    def __enter__(self) -> None:
        return

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        del exc_val, exc_tb

        # Save only if there is no exception.
        if exc_type is None:
            self.data_storage.save()
        return None


class DataStorageSectionStats(BaseModel):
    name: str
    amount: int


class DataStorage(BaseModel):
    path: Annotated[
        pathlib.Path | None,
        Field(description="Path to the data file. If `None`, storage is temporary. `None` must be explicit."),
    ]

    data: Data

    @classmethod
    def load(
        cls,
        dir_path: pathlib.Path | None,
    ) -> Self:
        if dir_path is None:
            return cls(path=None, data=Data())

        path = dir_path / "data.json"

        try:
            with path.open("r", encoding="utf-8") as file:
                data = Data.model_validate_json(file.read())
        except FileNotFoundError:
            data = Data()

        return cls(path=path, data=data)

    def save(self) -> None:
        if self.path is None:
            return

        dir_path = self.path.parent
        dir_path.mkdir(parents=True, exist_ok=True)

        with self.path.open("w", encoding="utf-8") as file:
            file.write(self.data.model_dump_json(indent=4, ensure_ascii=False))

    def autosave(self) -> DataStorageAutosaver:
        return DataStorageAutosaver(data_storage=self)

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
        with self.autosave():
            self.data.clear()

    def get_stats(self) -> list[DataStorageSectionStats]:
        return [
            DataStorageSectionStats(name="Contacts", amount=len(self.data.contacts)),
            DataStorageSectionStats(name="Notes", amount=len(self.data.notes)),
        ]
