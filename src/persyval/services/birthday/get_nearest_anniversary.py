import datetime
from typing import Final

from dateutil.relativedelta import relativedelta


def get_nearest_anniversary(birthday_date: datetime.date, current_date: datetime.date) -> datetime.date:
    # Note: Better handle for the leap years.
    # TODO: Better testing for leap years.
    year_diff = current_date.year - birthday_date.year
    contact_birthday_nearest_year = birthday_date + relativedelta(years=year_diff)

    if contact_birthday_nearest_year < current_date:
        contact_birthday_nearest_year += relativedelta(years=1)

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
