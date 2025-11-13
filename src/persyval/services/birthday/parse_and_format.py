import datetime
from typing import Final

FORMAT_BIRTHDAY_FOR_HUMAN: Final[str] = "YYYY-MM-DD"
"""ISO-8601 format for birthday."""

FORMAT_BIRTHDAY_FOR_EDIT: str = "%Y-%m-%d"
"""ISO-8601 format for birthday."""

# Format codes:
# https://docs.python.org/3.13/library/datetime.html#strftime-and-strptime-format-codes
FORMAT_BIRTHDAY_OUTPUT: str = "%d.%m.%Y %A"
"""Format for birthday output.

Use day of week.
"""


def format_birthday(birthday: datetime.date, date_format: str = FORMAT_BIRTHDAY_OUTPUT) -> str:
    return birthday.strftime(date_format)


def parse_birthday(birthday: str) -> datetime.date:
    return datetime.date.fromisoformat(birthday)
