import datetime
from typing import TYPE_CHECKING

from pydantic import BaseModel

from persyval.services.birthday.get_nearest_anniversary import get_nearest_anniversary, handle_weekend_birthday

if TYPE_CHECKING:
    from persyval.services.data_storage.data_storage import DataStorage


class AnniversaryContactInfo(BaseModel):
    name: str
    congratulation_date: datetime.date
    non_weekend_congratulation_date: datetime.date


def contacts_get_upcoming_birthdays(
    data_storage: DataStorage,
    target_days: int,
    *,
    sort: bool = False,
) -> list[AnniversaryContactInfo]:
    upcoming_birthdays = []

    # Ignore the timezone for this case for now.
    current_date = datetime.datetime.now().date()  # noqa: DTZ005

    for contact in data_storage.data.contacts.values():
        if not contact.birthday:
            continue

        nearest_birthday = get_nearest_anniversary(contact.birthday, current_date)
        days_until_birthday = (nearest_birthday - current_date).days

        if days_until_birthday > target_days:
            continue

        non_weekend_birthday = handle_weekend_birthday(nearest_birthday)

        upcoming_birthdays.append(
            AnniversaryContactInfo(
                name=contact.name,
                congratulation_date=nearest_birthday,
                non_weekend_congratulation_date=non_weekend_birthday,
            ),
        )

    if sort:
        upcoming_birthdays.sort(key=lambda x: x.congratulation_date)

    return upcoming_birthdays
