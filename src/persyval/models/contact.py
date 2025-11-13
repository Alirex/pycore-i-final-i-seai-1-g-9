import datetime
import uuid
from typing import TYPE_CHECKING, Annotated, Final, NewType

import phonenumbers
from email_validator import EmailNotValidError, validate_email
from prompt_toolkit import HTML
from pydantic import AfterValidator, BaseModel, ConfigDict, Field

from persyval.exceptions.main import InvalidDataError

if TYPE_CHECKING:
    from persyval.services.console.types import PromptToolkitFormattedText

ContactUid = NewType("ContactUid", uuid.UUID)

FORMAT_BIRTHDAY_FOR_HUMAN: Final[str] = "YYYY-MM-DD"
"""ISO-8601 format for birthday."""

DEFAULT_REGION = "UA"


def parse_birthday(birthday: str) -> datetime.date:
    return datetime.date.fromisoformat(birthday)


def format_birthday(birthday: datetime.date) -> str:
    return birthday.isoformat()


def validate_birthday(birthday: datetime.date) -> datetime.date:
    # TODO: validate birthday by minimal date.
    return birthday


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

    birthday: Annotated[datetime.date | None, AfterValidator(validate_birthday)] = None

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
