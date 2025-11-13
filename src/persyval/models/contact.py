import re
import uuid
from datetime import UTC, date, datetime, timedelta
from typing import TYPE_CHECKING, Annotated, Final, NewType

import phonenumbers
from email_validator import EmailNotValidError, validate_email
from prompt_toolkit import HTML
from pydantic import BaseModel, ConfigDict, Field, field_validator

from persyval.constants.numeric_contants import FIVE, ONE_HUNDRED, SIX, YEAR
from persyval.exceptions.main import InvalidDataError

if TYPE_CHECKING:
    from persyval.services.console.types import PromptToolkitFormattedText

ContactUid = NewType("ContactUid", uuid.UUID)

FORMAT_BIRTHDAY_FOR_HUMAN: Final[str] = "YYYY-MM-DD"
"""ISO-8601 format for birthday."""

DEFAULT_REGION = "UA"


def format_birthday(birthday: date) -> str:
    return birthday.isoformat()


def parse_birthday(birthday: date) -> str:
    return datetime.strftime(birthday, "%Y-%m-%d")


def validate_birthday(date_string: str) -> date:
    if isinstance(date_string, date):
        return date_string

    pattern = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
    valid_date_string_match = re.search(pattern, date_string.strip())
    if not valid_date_string_match:
        msg = "Invalid date format. Use YYYY-MM-DD"
        raise ValueError(msg)

    # Get current date and check approximate difference in years with it,
    # to prevent writting the future dates or dates more then 100 years old
    valid_date_string = datetime.strptime(
        valid_date_string_match.group(),
        "%Y-%m-%d",
    ).replace(tzinfo=UTC)
    current_date = datetime.now(UTC)
    difference = current_date - valid_date_string
    year_difference = difference.days // YEAR
    if not (0 < year_difference < ONE_HUNDRED):
        raise ValueError(
            "Birthday date can not be in future."
            if year_difference < 0
            else "Birthday date is invalid. Contact can not be more then 100 years old.",
        )

    return valid_date_string


def validate_phone_list(phones: list[str]) -> list[str]:
    validated = []

    for phone in phones:
        user_phone = phone.strip()
        if not user_phone:
            continue

        try:
            if user_phone.startswith("+"):
                parsed = phonenumbers.parse(user_phone, None)
            else:
                parsed = phonenumbers.parse(user_phone, DEFAULT_REGION)
        except phonenumbers.NumberParseException as e:
            msg = f"Invalid phone number format: {user_phone}"
            raise InvalidDataError(msg) from e

        if not phonenumbers.is_valid_number(parsed):
            msg = f"Invalid phone number: {user_phone}"
            raise InvalidDataError(msg)

        formatted = phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.E164,
        )
        validated.append(formatted)

    return list(set(validated))


def validate_email_list(emails: list[str]) -> list[str]:
    validated = []

    for email in emails:
        user_email = email.strip()
        if not user_email:
            continue

        try:
            valid = validate_email(user_email, check_deliverability=False)
            validated.append(valid.normalized)
        except EmailNotValidError as e:
            msg = f"Invalid email address: {user_email} ({e!s})"
            raise InvalidDataError(msg) from e

    return list(set(validated))


def get_nearest_anniversary(birthday_date: date, current_date: date) -> date:
    contact_birthday_nearest_year = datetime(
        year=current_date.year,
        month=birthday_date.month,
        day=birthday_date.day,
        tzinfo=UTC,
    ).date()
    is_birthday_this_year_passed = contact_birthday_nearest_year < current_date

    # Check user's birthday has already passed, set the birthday to next year
    if is_birthday_this_year_passed:
        contact_birthday_nearest_year = datetime(
            year=current_date.year + 1,
            month=birthday_date.month,
            day=birthday_date.day,
            tzinfo=UTC,
        ).date()

    return contact_birthday_nearest_year


def process_weekend_birthday(birthday_date: date) -> date:
    day_of_week = birthday_date.weekday()

    if day_of_week in {FIVE, SIX}:
        interval = 2 if day_of_week == FIVE else 1
        birthday_date += timedelta(days=interval)

    return birthday_date


TRIM_ADDRESS: Final[int] = 10
LONG_PLACEHOLDER: Final[str] = "..."

ALLOWED_KEYS_TO_FILTER: Final[set[str]] = {"uid", "name", "address", "phones", "emails"}


class Contact(BaseModel):
    uid: ContactUid = Field(default_factory=lambda: ContactUid(uuid.uuid7()))

    name: Annotated[str, Field(description="The name of the contact.", min_length=1)]

    address: Annotated[str | None, Field(description="The address of the contact.")] = None

    # TODO: Use fields: email, phone (maybe multiple)

    phones: list[str] = Field(
        default_factory=list,
        description="List of phone numbers associated with the contact.",
    )
    #
    emails: list[str] = Field(
        default_factory=list,
        description="List of email addresses associated with the contact.",
    )

    birthday: date | None = None
    _validate_birthday = field_validator("birthday", mode="before")(validate_birthday)

    model_config = ConfigDict(
        validate_assignment=True,
    )

    def get_prompt_toolkit_output(self) -> PromptToolkitFormattedText:
        text = f"<b>{self.name}</b>"

        address = self.address or ""
        if len(address) > TRIM_ADDRESS:
            size = TRIM_ADDRESS - len(LONG_PLACEHOLDER)
            address = f"{address[:size]}{LONG_PLACEHOLDER}"

        if address:
            text += f", {address}"

        if self.birthday:
            text += f" ({format_birthday(self.birthday)})"

        # TODO: Need to decide Do we need to show phones and emails in prompt?
        # if self.phones:
        #     text += f" {self.phones}"

        # if self.emails:
        #     text += f" {self.emails}"

        text += f"  (<i>{self.uid}</i>)"

        return HTML(text)
