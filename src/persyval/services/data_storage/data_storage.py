import pathlib
from datetime import UTC, date, datetime
from typing import TYPE_CHECKING, Self, cast

from pydantic import BaseModel, Field

from persyval.models.contact import Contact, ContactUid
from persyval.models.note import Note, NoteUid

if TYPE_CHECKING:
    from types import TracebackType

from persyval.models.contact import get_nearest_anniversary, process_weekend_birthday

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

    def get_upcoming_birthdays(self, target_days: int) -> list[dict[str, str | date]]:
        upcoming_birthdays = []
        current_date = datetime.now(UTC).date()

        for contact in self.data.contacts.values():
            if not contact.birthday:
                continue

            nearest_birthday = get_nearest_anniversary(contact.birthday, current_date)
            days_until_birthday = (nearest_birthday - current_date).days

            if not days_until_birthday <= target_days:
                continue

            # Move weekend birthdays to Monday
            non_weekend_birthday = process_weekend_birthday(nearest_birthday)
            upcoming_birthdays.append(
                {
                    "name": contact.name,
                    "congratulation date": nearest_birthday,
                    "non-weekend congratulation date": non_weekend_birthday,
                },
            )

        return cast("list[dict[str, str | date]]", upcoming_birthdays)
