import datetime
import uuid
from typing import TYPE_CHECKING, Annotated, Final, NewType

from prompt_toolkit import HTML
from pydantic import AfterValidator, BaseModel, ConfigDict, Field

from persyval.constants.numeric_contants import FIVE, SIX
from persyval.services.birthday.parse_and_format import format_birthday
from persyval.services.birthday.validate_birthday import validate_birthday

if TYPE_CHECKING:
    from persyval.services.console.types import PromptToolkitFormattedText

ContactUid = NewType("ContactUid", uuid.UUID)


def get_nearest_anniversary(birthday_date: datetime.date, current_date: datetime.date) -> datetime.date:
    contact_birthday_nearest_year = datetime.datetime(
        year=current_date.year,
        month=birthday_date.month,
        day=birthday_date.day,
        tzinfo=datetime.UTC,
    ).date()
    is_birthday_this_year_passed = contact_birthday_nearest_year < current_date

    # Check user's birthday has already passed, set the birthday to next year
    if is_birthday_this_year_passed:
        contact_birthday_nearest_year = datetime.datetime(
            year=current_date.year + 1,
            month=birthday_date.month,
            day=birthday_date.day,
            tzinfo=datetime.UTC,
        ).date()

    return contact_birthday_nearest_year


def process_weekend_birthday(birthday_date: datetime.date) -> datetime.date:
    day_of_week = birthday_date.weekday()

    if day_of_week in {FIVE, SIX}:
        interval = 2 if day_of_week == FIVE else 1
        birthday_date += datetime.timedelta(days=interval)

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

    birthday: Annotated[
        datetime.date | None,
        AfterValidator(validate_birthday),
    ] = None

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
