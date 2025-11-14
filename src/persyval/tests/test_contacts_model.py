import datetime

import pytest

from persyval.models.contact import Contact


def test_contact_create_i_simple() -> None:
    Contact(
        name="Test",
    )


def test_contact_create_i_bad_name() -> None:
    with pytest.raises(ValueError, match="String should have at least"):
        Contact(
            name="",
        )


def test_contact_create_i_simple_more_args() -> None:
    Contact(
        name="Test",
        address="Test",
    )


@pytest.mark.parametrize(
    "birthday",
    [
        "1991-01-01",
        datetime.date(1991, 1, 1),
        None,
    ],
)
def test_contact_create_i_different_formats(birthday: str | datetime.date | None) -> None:
    Contact(
        name="Test",
        address="Test",
        birthday=birthday,  # type: ignore[arg-type]
    )


def test_contact_create_i_phones_emails() -> None:
    Contact(
        name="Test",
        address="Test",
        phones=[
            "+380731234567",
        ],
        emails=[
            "a@a.com",
        ],
    )
