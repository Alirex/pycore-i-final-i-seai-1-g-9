import datetime
from typing import Final

from dateutil.relativedelta import relativedelta

from persyval.exceptions.main import InvalidDataError

MAX_AGE: Final[int] = 200
"""Maximum age limit for a birthday date validation.

This constant is set to prevent unrealistic birthday dates.

We have to be careful with this limit, because it can be
changed in the future.

Also, now we have at least 100 years old people.

In future, we can have broken system, if someone will be
older than this limit.
"""


def validate_birthday(date: datetime.date | None) -> datetime.date | None:
    """Validate birthday date.

    It must be:
    - not in the future
    - respect the age limit
    """
    if not date:
        return None

    # Ignore time zone for this case.
    current_date = datetime.datetime.now().date()  # noqa: DTZ005

    if date > current_date:
        msg = "Birthday date can not be in future."
        raise InvalidDataError(msg)

    # Check age limit.
    difference = relativedelta(current_date, date)
    if difference.years > MAX_AGE:
        msg = "Birthday date is invalid. Contact can not be more then 100 years old."
        raise InvalidDataError(msg)

    return date
