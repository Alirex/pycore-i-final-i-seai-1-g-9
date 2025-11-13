import datetime
import uuid
from typing import TYPE_CHECKING, Annotated, Final, NewType

from prompt_toolkit import HTML
from pydantic import AfterValidator, BaseModel, ConfigDict, Field

from persyval.services.birthday.parse_and_format import format_birthday
from persyval.services.birthday.validate_birthday import validate_birthday

if TYPE_CHECKING:
    from persyval.services.console.types import PromptToolkitFormattedText

ContactUid = NewType("ContactUid", uuid.UUID)

TRIM_ADDRESS: Final[int] = 10
LONG_PLACEHOLDER: Final[str] = "..."

ALLOWED_KEYS_TO_FILTER: Final[set[str]] = {"uid", "name", "address", "phones", "emails"}


class Contact(BaseModel):
    uid: ContactUid = Field(default_factory=lambda: ContactUid(uuid.uuid7()))

    name: Annotated[str, Field(description="The name of the contact.", min_length=1)]

    address: Annotated[str | None, Field(description="The address of the contact.")] = None

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
