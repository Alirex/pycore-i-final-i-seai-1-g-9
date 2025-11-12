import datetime
import uuid
from typing import TYPE_CHECKING, Annotated, Final, NewType

from prompt_toolkit import HTML
from pydantic import AfterValidator, BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from persyval.services.console.types import PromptToolkitFormattedText

ContactUid = NewType("ContactUid", uuid.UUID)


def parse_birthday(birthday: str) -> datetime.date:
    return datetime.date.fromisoformat(birthday)


def format_birthday(birthday: datetime.date) -> str:
    return birthday.isoformat()


def validate_birthday(birthday: datetime.date) -> datetime.date:
    # TODO: validate birthday by minimal date.
    return birthday


TRIM_ADDRESS: Final[int] = 10
LONG_PLACEHOLDER: Final[str] = "..."


class Contact(BaseModel):
    uid: ContactUid = Field(default_factory=lambda: ContactUid(uuid.uuid7()))

    name: Annotated[str, Field(description="The name of the contact.", min_length=1)]

    address: Annotated[str | None, Field(description="The address of the contact.")] = None

    # TODO: Use fields: email, phone (maybe multiple)

    # phones: list[Phone] = Field(
    #     default_factory=list,
    #     description="List of phone numbers associated with the contact.",
    # )
    #
    # email: EmailStr

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

        return HTML(text)
