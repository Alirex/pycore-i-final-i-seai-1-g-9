import datetime
from typing import TYPE_CHECKING, Annotated

from pydantic import BaseModel, Field

from persyval.models.contact import (
    Contact,
)
from persyval.services.birthday.parse_and_format import FORMAT_BIRTHDAY_FOR_HUMAN, parse_birthday
from persyval.services.birthday.validate_birthday import validate_birthday
from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig, ArgType
from persyval.services.data_actions.contact_add import contact_add
from persyval.services.email.validate_email import validate_email_list
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.services.phone.validate_phone_list import validate_phone_list
from persyval.utils.format import render_good_message

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput


class ContactAddIArgs(BaseModel):
    name: str
    address: str | None = None
    birthday: datetime.date | None = None

    phones: Annotated[list[str], Field(default_factory=list)]
    emails: Annotated[list[str], Field(default_factory=list)]


CONTACT_ADD_I_ARGS_CONFIG = ArgsConfig[ContactAddIArgs](
    result_cls=ContactAddIArgs,
    args=[
        ArgMetaConfig(
            name="name",
            required=True,
        ),
        ArgMetaConfig(
            name="address",
        ),
        ArgMetaConfig(
            name="birthday",
            type_=ArgType.DATE,
            format=FORMAT_BIRTHDAY_FOR_HUMAN,
            parser_func=parse_birthday,
            validator_func=validate_birthday,
        ),
        ArgMetaConfig(
            name="phones",
            type_=ArgType.LIST_BY_COMMA,
            validator_func=validate_phone_list,
        ),
        ArgMetaConfig(
            name="emails",
            type_=ArgType.LIST_BY_COMMA,
            validator_func=validate_email_list,
        ),
    ],
)


class ContactAddIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        parsed_args = CONTACT_ADD_I_ARGS_CONFIG.parse(self.args)
        self._make_action(parsed_args)
        return None

    def parsed_call(self, parsed_args: ContactAddIArgs) -> None:
        self._make_action(parsed_args)

    def _make_action(self, parsed_args: ContactAddIArgs) -> None:
        # TODO: Implement

        # name = prompt(HTML("Enter <b>name</b>: "))
        # address = prompt(HTML("Enter <b>address</b> <i>(Optional)</i>: ")) or None
        # birthday = prompt(HTML("Enter <b>birthday</b> <i>(Optional)(YYYY-MM-DD)</i>: ")) or None

        contact = Contact(
            name=parsed_args.name,
            address=parsed_args.address,
            birthday=parsed_args.birthday,
            phones=parsed_args.phones,
            emails=parsed_args.emails,
        )

        contact_add(data_storage=self.data_storage, contact=contact)

        render_good_message(
            self.console,
            f"Contact '{contact.name}' added successfully.",
        )
