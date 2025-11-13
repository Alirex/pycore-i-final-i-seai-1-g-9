import datetime
from typing import Final

FORMAT_BIRTHDAY_FOR_HUMAN: Final[str] = "YYYY-MM-DD"
"""ISO-8601 format for birthday."""

# Format codes:
# https://docs.python.org/3.13/library/datetime.html#strftime-and-strptime-format-codes
FORMAT_BIRTHDAY_OUTPUT: str = "%d.%m.%Y %A"
"""Format for birthday output.

Use day of week.
"""


def format_birthday(birthday: datetime.date) -> str:
    return birthday.strftime(FORMAT_BIRTHDAY_OUTPUT)


def parse_birthday(birthday: str) -> datetime.date:
    return datetime.date.fromisoformat(birthday)
