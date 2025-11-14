import pytest

from persyval.exceptions.main import EmptyDataError, InvalidDataError
from persyval.services.email.validate_email import (
    parse_emails,
    validate_email,
    validate_email_list,
)


@pytest.mark.parametrize(
    ("input_str", "expected"),
    [
        ("a@example.com,b@example.com", ["a@example.com", "b@example.com"]),
        ("a@example.com, b@example.com", ["a@example.com", " b@example.com"]),
        (",a@example.com,", ["a@example.com"]),
        ("", []),
        (" , , , ", [" ", " ", " ", " "]),
        ("one@example.com,,two@example.com,,", ["one@example.com", "two@example.com"]),
        ("single@example.com", ["single@example.com"]),
        (",,,", []),
        (
            "email1@example.com,email2@example.com,email3@example.com",
            ["email1@example.com", "email2@example.com", "email3@example.com"],
        ),
        (" ,email@example.com, ", [" ", "email@example.com", " "]),
    ],
)
def test_parse_emails(input_str: str, expected: list[str]) -> None:
    result = parse_emails(input_str)
    assert result == expected


@pytest.mark.parametrize(
    ("email", "expected"),
    [
        ("Test@Example.Com", "Test@example.com"),
        ("   User@Gmail.com   ", "User@gmail.com"),
        ("MiXeD@Yandex.RU", "MiXeD@yandex.ru"),
        ("simple@mail.ua", "simple@mail.ua"),
        ("Another.Test@domain.co.uk", "Another.Test@domain.co.uk"),
        ("USER123@Sub.Domain.COM", "USER123@sub.domain.com"),
        ("nospaces@example.com", "nospaces@example.com"),
        ("   mixedCASE@Example.Org   ", "mixedCASE@example.org"),
    ],
)
def test_validate_email_valid(email: str, expected: str) -> None:
    result = validate_email(email)
    assert result == expected


@pytest.mark.parametrize(
    "email",
    [
        "bad-email",
        "user@",
        "@example.com",
        "user@@gmail.com",
        "user@example..com",
        "a@b",
        "noatsymbol.com",
        "user@.com",
        ".user@example.com",
        "user@com.",
        "user@domain,com",
        "user@domain..com",
    ],
)
def test_validate_email_invalid(email: str) -> None:
    with pytest.raises(InvalidDataError):
        validate_email(email)


@pytest.mark.parametrize(
    "email",
    [
        "",
        "   ",
    ],
)
def test_validate_email_empty(email: str) -> None:
    with pytest.raises(EmptyDataError):
        validate_email(email)


def test_validate_email_list_valid() -> None:
    emails = [
        "A@Example.com",
        "b@example.com",
        "a@example.com",
        "User@Gmail.com",
        "user@gmail.com",
    ]
    result = validate_email_list(emails)
    assert result == [
        "A@example.com",
        "b@example.com",
        "a@example.com",
        "User@gmail.com",
        "user@gmail.com",
    ]


def test_validate_email_list_invalid() -> None:
    emails = ["good@example.com", "bad-email", "other@example.com"]
    with pytest.raises(InvalidDataError):
        validate_email_list(emails)


def test_validate_email_list_all_valid_no_duplicates() -> None:
    emails = ["one@example.com", "two@example.com", "three@example.com"]
    result = validate_email_list(emails)
    assert result == ["one@example.com", "two@example.com", "three@example.com"]


def test_validate_email_list_all_invalid() -> None:
    emails = ["bad-email", "wrong@", "@domain", " "]
    with pytest.raises(InvalidDataError):
        validate_email_list(emails)


def test_validate_email_list_mixed_valid_invalid() -> None:
    emails = ["valid1@example.com", "invalid@", "Valid2@domain.com"]
    with pytest.raises(InvalidDataError):
        validate_email_list(emails)


def test_validate_email_list_with_duplicates() -> None:
    emails = ["dup@example.com", "Dup@example.com", "dup@example.com", "unique@domain.com"]
    result = validate_email_list(emails)
    assert result == ["dup@example.com", "Dup@example.com", "unique@domain.com"]


def test_validate_email_list_all_valid_with_spaces() -> None:
    emails = ["  spaced@example.com  ", "trim@domain.com"]
    result = validate_email_list(emails)
    assert result == ["spaced@example.com", "trim@domain.com"]
