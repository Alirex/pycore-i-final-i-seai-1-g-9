import datetime
from typing import cast

import pytest

from persyval.services.birthday.get_nearest_anniversary import (
    birthday_in_year,
    get_nearest_anniversary,
    handle_weekend_birthday,
    is_leap_year,
)
from persyval.services.birthday.parse_and_format import (
    format_birthday_for_edit,
    format_birthday_for_output,
    parse_birthday,
)
from persyval.services.birthday.validate_birthday import validate_birthday

DAYS_IN_YEAR = 365


# Region: parse_birthday tests
@pytest.mark.parametrize(
    ("birthday", "expected"),
    [
        ("1990-01-01", datetime.date(1990, 1, 1)),
        ("2000-02-29", datetime.date(2000, 2, 29)),
    ],
)
def test_parse_birthday(birthday: str, expected: datetime.date) -> None:
    result = parse_birthday(birthday)
    assert result == expected


@pytest.mark.parametrize(
    "birthday_str",
    [
        "01-01-1990",
        "1990-01-01-00-00",
        "1990 01 01",
        "bla",
    ],
)
def test_parse_birthday_i_invalid_format(birthday_str: str) -> None:
    with pytest.raises(ValueError, match="Invalid isoformat"):
        parse_birthday(birthday_str)


@pytest.mark.parametrize(
    "birthday",
    [
        "",
        None,
    ],
)
def test_parse_birthday_i_empty(birthday: str | None) -> None:
    result = parse_birthday(birthday)
    assert result is None


# Region: format_birthday_for_output tests
@pytest.mark.parametrize(
    ("birthday", "expected"),
    [
        (datetime.date(1991, 12, 31), "1991-12-31 Tuesday"),
        (datetime.date(2000, 1, 1), "2000-01-01 Saturday"),
    ],
)
def test_format_birthday_for_output(birthday: datetime.date, expected: str) -> None:
    result = format_birthday_for_output(birthday)
    assert result == expected


@pytest.mark.parametrize(
    "birthday",
    [
        "1990-01-01",
        12345,
        None,
        datetime.datetime(2020, 1, 1, tzinfo=datetime.UTC),  # datetime instead of date (tz-aware)
    ],
)
def test_format_birthday_for_output_invalid_input_type(birthday: object) -> None:
    with pytest.raises(TypeError, match=r".*"):
        format_birthday_for_output(cast("datetime.date", birthday))


# Region: format_birthday_for_edit tests
@pytest.mark.parametrize(
    ("birthday", "expected"),
    [
        (datetime.date(1991, 12, 31), "1991-12-31"),
        (datetime.date(2000, 1, 1), "2000-01-01"),
        (datetime.date(2024, 2, 29), "2024-02-29"),  # leap year
    ],
)
def test_format_birthday_for_edit_valid(birthday: datetime.date, expected: str) -> None:
    result = format_birthday_for_edit(birthday)
    assert result == expected


@pytest.mark.parametrize(
    "birthday",
    [
        "1990-01-01",
        12345,
        None,
    ],
)
def test_format_birthday_for_edit_invalid(birthday: object) -> None:
    with pytest.raises((TypeError, ValueError)):
        format_birthday_for_edit(cast("datetime.date", birthday))


# Region: is_leap_year tests
@pytest.mark.parametrize(
    ("year", "expected"),
    [
        (2000, True),
        (2021, False),
    ],
)
def test_is_leap_year_valid(year: int, expected: bool) -> None:  # noqa: FBT001
    assert is_leap_year(year) is expected


# Region: birthday_in_year tests
@pytest.mark.parametrize(
    ("birthday", "year", "expected"),
    [
        # Regular birthday
        (datetime.date(1990, 5, 15), 2025, datetime.date(2025, 5, 15)),
        # Feb 29 on leap year
        (datetime.date(2000, 2, 29), 2024, datetime.date(2024, 2, 29)),
        # Feb 29 on non-leap year → fallback to Feb 28
        (datetime.date(2000, 2, 29), 2025, datetime.date(2025, 2, 28)),
    ],
)
def test_birthday_in_year_valid(birthday: datetime.date, year: int, expected: datetime.date) -> None:
    assert birthday_in_year(birthday, year) == expected


@pytest.mark.parametrize(
    ("birthday", "year"),
    [
        ("2000-02-29", 2024),
        (None, 2024),
        (datetime.date(2000, 2, 29), None),
    ],
)
def test_birthday_in_year_invalid(birthday: object, year: object) -> None:
    with pytest.raises((TypeError, AttributeError)):
        birthday_in_year(cast("datetime.date", birthday), cast("int", year))


# Region: get_nearest_anniversary tests
@pytest.mark.parametrize(
    ("birthday_date", "current_date", "expected"),
    [
        # Birthday later this year
        (datetime.date(1990, 12, 31), datetime.date(2025, 1, 1), datetime.date(2025, 12, 31)),
        # Birthday already passed this year
        (datetime.date(1990, 1, 1), datetime.date(2025, 12, 31), datetime.date(2026, 1, 1)),
        # Birthday today
        (datetime.date(2000, 5, 20), datetime.date(2025, 5, 20), datetime.date(2025, 5, 20)),
        # Leap year birthday, current year is not leap
        (datetime.date(2000, 2, 29), datetime.date(2025, 3, 1), datetime.date(2026, 2, 28)),
    ],
)
def test_get_nearest_anniversary_valid(
    birthday_date: datetime.date,
    current_date: datetime.date,
    expected: datetime.date,
) -> None:
    result = get_nearest_anniversary(birthday_date, current_date)
    assert result == expected


@pytest.mark.parametrize(
    ("birthday_date", "current_date"),
    [
        ("1990-01-01", datetime.date(2025, 1, 1)),
        (datetime.date(1990, 1, 1), None),
        (123, datetime.date(2025, 1, 1)),
    ],
)
def test_get_nearest_anniversary_invalid(birthday_date: object, current_date: object) -> None:
    with pytest.raises((TypeError, ValueError, AttributeError)):
        get_nearest_anniversary(cast("datetime.date", birthday_date), cast("datetime.date", current_date))


# Region: handle_weekend_birthday tests
@pytest.mark.parametrize(
    ("birthday", "expected"),
    [
        # Birthday on Saturday -> moved to Monday
        (datetime.date(2025, 1, 4), datetime.date(2025, 1, 6)),  # Saturday -> Monday
        # Birthday on Sunday -> moved to Monday
        (datetime.date(2025, 1, 5), datetime.date(2025, 1, 6)),  # Sunday -> Monday
        # Birthday on Monday -> stays same
        (datetime.date(2025, 1, 6), datetime.date(2025, 1, 6)),  # Monday
    ],
)
def test_handle_weekend_birthday_valid(birthday: datetime.date, expected: datetime.date) -> None:
    assert handle_weekend_birthday(birthday) == expected


@pytest.mark.parametrize(
    "invalid_input",
    [
        "2025-01-04",
        None,
    ],
)
def test_handle_weekend_birthday_invalid(invalid_input: object) -> None:
    with pytest.raises((AttributeError, TypeError)):
        handle_weekend_birthday(cast("datetime.date", invalid_input))


# Region: validate_birthday tests
@pytest.mark.parametrize(
    ("birthday", "expected"),
    [
        (None, None),  # None input
        (
            datetime.datetime.now(datetime.UTC).date(),
            datetime.datetime.now(datetime.UTC).date(),
        ),  # today (tz-aware now)
        (
            datetime.datetime.now(datetime.UTC).date()
            - datetime.timedelta(
                days=25 * DAYS_IN_YEAR,
            ),
            datetime.datetime.now(datetime.UTC).date()
            - datetime.timedelta(
                days=25 * DAYS_IN_YEAR,
            ),
        ),
    ],
)
def test_validate_birthday_valid(birthday: object, expected: object) -> None:
    assert validate_birthday(cast("datetime.date | None", birthday)) == expected
