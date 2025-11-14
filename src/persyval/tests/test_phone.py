import pytest

from persyval.exceptions.main import InvalidDataError
from persyval.services.phone.validate_phone_list import (
    parse_phones,
    validate_phone,
    validate_phone_list,
)


@pytest.mark.parametrize(
    ("input_str", "expected"),
    [
        ("+380671234567,+380501112233", ["+380671234567", "+380501112233"]),
        ("0671234567,0501112233", ["0671234567", "0501112233"]),
        (",0671234567,", ["0671234567"]),
        ("", []),
        (" , , , ", [" ", " ", " ", " "]),
        ("+380671234567,,+380501112233,,", ["+380671234567", "+380501112233"]),
        ("single+380671234567", ["single+380671234567"]),
        (",,,", []),
        ("+380671234567,+380501112233,+380631112244", ["+380671234567", "+380501112233", "+380631112244"]),
        (" ,+380671234567, ", [" ", "+380671234567", " "]),
        ("0671234567,0501234567", ["0671234567", "0501234567"]),
    ],
)
def test_parse_phones(input_str: str, expected: list[str]) -> None:
    result = parse_phones(input_str)
    assert result == expected


@pytest.mark.parametrize(
    ("phone", "expected"),
    [
        ("+380671234567", "+380671234567"),
        ("0671234567", "0671234567"),
        ("0501112233", "0501112233"),
        ("+380501112233", "+380501112233"),
        ("+380631112244", "+380631112244"),
    ],
)
def test_validate_phone_valid(phone: str, expected: str) -> None:
    result = validate_phone(phone)
    assert result == expected


@pytest.mark.parametrize(
    "phone",
    [
        "",
        "   ",
        "123",
        "+999999999999",
        "abcdefg",
        "+3805011122",
        "050111223344",
        "0000000",
        "++1234567890",
    ],
)
def test_validate_phone_invalid(phone: str) -> None:
    with pytest.raises(InvalidDataError):
        validate_phone(phone)


def test_validate_phone_list_valid() -> None:
    phones = ["+380671234567", "0671234567", "+380501112233", "0501112233"]
    result = validate_phone_list(phones)
    assert result == ["+380671234567", "0671234567", "+380501112233", "0501112233"]


def test_validate_phone_list_invalid() -> None:
    phones = ["+380671234567", "badphone", "0501112233"]
    with pytest.raises(InvalidDataError):
        validate_phone_list(phones)


def test_validate_phone_list_all_valid_no_duplicates() -> None:
    phones = ["+380671234567", "0671234567", "0501112233"]
    result = validate_phone_list(phones)
    assert result == ["+380671234567", "0671234567", "0501112233"]


def test_validate_phone_list_all_invalid() -> None:
    phones = ["", "123", "abcdefg"]
    with pytest.raises(InvalidDataError):
        validate_phone_list(phones)


def test_validate_phone_list_mixed_valid_invalid() -> None:
    phones = ["+380671234567", "invalid", "0501112233"]
    with pytest.raises(InvalidDataError):
        validate_phone_list(phones)


def test_validate_phone_list_with_duplicates() -> None:
    phones = ["+380671234567", "0671234567", "+380671234567", "0501112233"]
    result = validate_phone_list(phones)
    assert result == ["+380671234567", "0671234567", "0501112233"]


def test_validate_phone_list_all_valid_with_spaces() -> None:
    phones = ["0671234567", " +380501112233 "]
    result = validate_phone_list(phones)
    assert result == ["0671234567", "+380501112233"]
