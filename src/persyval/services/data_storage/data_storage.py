import datetime
import pathlib
import uuid
from typing import TYPE_CHECKING, Annotated, NewType, Self

from pydantic import BaseModel, EmailStr, Field

from persyval.models.phone import Phone

if TYPE_CHECKING:
    from types import TracebackType

ContactName = NewType("ContactName", str)

ContactUid = NewType("ContactUid", uuid.UUID)


class Contact(BaseModel):
    uid: ContactUid = Field(default_factory=lambda: ContactUid(uuid.uuid7()))

    name: Annotated[ContactName, Field(description="The name of the contact.", min_length=1)]

    address: Annotated[str | None, Field(description="The address of the contact.")] = None

    phones: list[Phone] = Field(
        default_factory=list,
        description="List of phone numbers associated with the contact.",
    )

    email: EmailStr

    birthday: datetime.date


NoteUid = NewType("NoteUid", uuid.UUID)


class Note(BaseModel):
    uid: NoteUid = Field(default_factory=lambda: NoteUid(uuid.uuid7()))
    title: str
    content: str


class Data(BaseModel):
    contacts: dict[ContactUid, Contact] = Field(
        default_factory=dict,
        description="Dictionary of contacts indexed by their unique identifiers.",
    )

    notes: dict[NoteUid, Note] = Field(
        default_factory=dict,
        description="Dictionary of notes indexed by their unique identifiers.",
    )


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
