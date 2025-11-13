import datetime
from typing import Final

FORMAT_BIRTHDAY_FOR_HUMAN: Final[str] = "YYYY-MM-DD"
"""ISO-8601 format for birthday."""


def format_birthday(birthday: datetime.date) -> str:
    return birthday.isoformat()


def parse_birthday(birthday: str) -> datetime.date:
    return datetime.date.fromisoformat(birthday)
