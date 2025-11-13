import datetime

import pytest

from persyval.services.birthday.parse_and_format import parse_birthday


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
        "",
    ],
)
def test_parse_birthday_i_invalid_format(birthday_str: str) -> None:
    with pytest.raises(ValueError, match="Invalid isoformat"):
        parse_birthday(birthday_str)
