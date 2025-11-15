import datetime
import enum
import uuid
from functools import cache
from typing import TYPE_CHECKING, Annotated, Final, NewType

from prompt_toolkit import HTML
from pydantic import AfterValidator, BaseModel, ConfigDict, Field, field_serializer

from persyval.services.birthday.parse_and_format import format_birthday_for_edit_and_export, format_birthday_for_output
from persyval.services.birthday.validate_birthday import validate_birthday
from persyval.services.email.validate_email import validate_email_list
from persyval.services.model_meta.model_meta_info import ModelMetaInfo
from persyval.services.phone.validate_phone_list import validate_phone_list

if TYPE_CHECKING:
    from persyval.services.console.types import PromptToolkitFormattedText

ContactUid = NewType("ContactUid", uuid.UUID)

TRIM_ADDRESS: Final[int] = 10
LONG_PLACEHOLDER: Final[str] = "..."


class AllowedKeysToFilter(enum.StrEnum):
    UID = "uid"
    NAME = "name"
    ADDRESS = "address"
    BIRTHDAY = "birthday"

    # Special. Because of the singular form.
    PHONE = "phone"
    EMAIL = "email"


ALLOWED_KEYS_TO_FILTER: Final[set[str]] = set(AllowedKeysToFilter)

ENTITY_PUBLIC_NAME: Final[str] = "Contact"


class Contact(BaseModel):
    uid: ContactUid = Field(default_factory=lambda: ContactUid(uuid.uuid7()))

    name: Annotated[str, Field(description="The name of the contact.", min_length=1)]

    address: Annotated[str | None, Field(description="The address of the contact.")] = None

    # noinspection Pydantic
    phones: Annotated[
        list[str],
        AfterValidator(validate_phone_list),
    ] = Field(
        default_factory=list,
        description="List of phone numbers associated with the contact.",
    )
    # noinspection Pydantic
    emails: Annotated[
        list[str],
        AfterValidator(validate_email_list),
    ] = Field(
        default_factory=list,
        description="List of email addresses associated with the contact.",
    )

    birthday: Annotated[
        datetime.date | None,
        AfterValidator(validate_birthday),
    ] = None

    @field_serializer("birthday")
    def serialize_birthday(self, birthday: datetime.date | None) -> str | None:
        return format_birthday_for_edit_and_export(birthday) if birthday else None

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
            text += f" ({format_birthday_for_output(self.birthday)})"

        # TODO: Need to decide Do we need to show phones and emails in prompt?
        # if self.phones:
        #     text += f" {self.phones}"

        # if self.emails:
        #     text += f" {self.emails}"

        text += f"  (<i>{self.uid}</i>)"

        return HTML(text)

    @classmethod
    @cache
    def get_meta_info(cls) -> ModelMetaInfo:
        return ModelMetaInfo.from_class(cls)
