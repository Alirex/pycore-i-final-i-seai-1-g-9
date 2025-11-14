import datetime
from typing import Final

FEBRUARY_MONTH = 2
LEAP_DAY = 29
NON_LEAP_DAY = 28


def is_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def birthday_in_year(birthday_date: datetime.date, year: int) -> datetime.date:
    if birthday_date.month == FEBRUARY_MONTH and birthday_date.day == LEAP_DAY:
        day = LEAP_DAY if is_leap_year(year) else NON_LEAP_DAY
        return datetime.date(year, 2, day)
    return birthday_date.replace(year=year)


def get_nearest_anniversary(birthday_date: datetime.date, current_date: datetime.date) -> datetime.date:
    contact_birthday_nearest_year = birthday_in_year(birthday_date, current_date.year)

    if contact_birthday_nearest_year < current_date:
        contact_birthday_nearest_year = birthday_in_year(birthday_date, current_date.year + 1)

    return contact_birthday_nearest_year


# 0 - Monday, 6 - Sunday
WEEKDAY_I_MONDAY: Final[int] = 0
WEEKDAY_I_SATURDAY: Final[int] = 5
WEEKDAY_I_SUNDAY: Final[int] = 6

DAYS_IN_WEEK: Final[int] = 7

WEEKDAY_TO_MOVE_FROM: set[int] = {
    WEEKDAY_I_SATURDAY,
    WEEKDAY_I_SUNDAY,
}

WEEKDAY_TO_MOVE_TO: Final[int] = WEEKDAY_I_MONDAY


def handle_weekend_birthday(birthday_date: datetime.date) -> datetime.date:
    """Move weekend birthdays to the next Monday, if needed."""
    day_of_week = birthday_date.weekday()

    if day_of_week in WEEKDAY_TO_MOVE_FROM:
        days_to_monday = (WEEKDAY_TO_MOVE_TO - day_of_week) % DAYS_IN_WEEK
        birthday_date += datetime.timedelta(days=days_to_monday)

    return birthday_date
