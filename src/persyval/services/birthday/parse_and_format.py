import datetime
from typing import Final

FORMAT_BIRTHDAY_FOR_HUMAN: Final[str] = "YYYY-MM-DD"
"""ISO-8601 format for birthday."""


# Format codes:
# https://docs.python.org/3.13/library/datetime.html#strftime-and-strptime-format-codes
FORMAT_BIRTHDAY_OUTPUT: str = "%Y-%m-%d %A"
"""Format for birthday output.

Use day of week.

YYYY-MM-DD Weekday
1991-12-31 Monday
"""


def format_birthday_for_output(birthday: datetime.date) -> str:
    return birthday.strftime(FORMAT_BIRTHDAY_OUTPUT)


def format_birthday_for_edit(birthday: datetime.date) -> str:
    return birthday.isoformat()


def parse_birthday(birthday: str | None) -> datetime.date | None:
    return datetime.date.fromisoformat(birthday) if birthday else None
