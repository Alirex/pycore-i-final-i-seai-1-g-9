import datetime

from pydantic import Field

from persyval.models.contact import (
    Contact,
)
from persyval.services.birthday.parse_and_format import FORMAT_BIRTHDAY_FOR_HUMAN, parse_birthday
from persyval.services.birthday.validate_birthday import validate_birthday
from persyval.services.commands.args_config import ArgMetaConfig, ArgsConfig, ArgType
from persyval.services.data_actions.contact_add import contact_add
from persyval.services.email.validate_email import validate_email_list
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.services.phone.validate_phone_list import validate_phone_list
from persyval.utils.format import render_good_message


class ContactAddIArgs(HandlerArgsBase):
    name: str | None = None
    address: str | None = None
    birthday: datetime.date | None = None

    phones: list[str] = Field(default_factory=list)
    emails: list[str] = Field(default_factory=list)


CONTACT_ADD_I_ARGS_CONFIG = ArgsConfig[ContactAddIArgs](
    result_cls=ContactAddIArgs,
    args=[
        ArgMetaConfig(
            name="name",
            required=True,
            allow_input_on_empty=True,
        ),
        ArgMetaConfig(
            name="address",
            allow_input_on_empty=True,
        ),
        ArgMetaConfig(
            name="birthday",
            type_=ArgType.DATE,
            format=FORMAT_BIRTHDAY_FOR_HUMAN,
            parser_func=parse_birthday,
            validator_func=validate_birthday,
            allow_input_on_empty=True,
        ),
        ArgMetaConfig(
            name="phones",
            type_=ArgType.LIST_BY_COMMA,
            validator_func=validate_phone_list,
            allow_input_on_empty=True,
        ),
        ArgMetaConfig(
            name="emails",
            type_=ArgType.LIST_BY_COMMA,
            validator_func=validate_email_list,
            allow_input_on_empty=True,
        ),
    ],
)


class ContactAddIHandler(
    HandlerBase[ContactAddIArgs],
):
    def _get_args_config(self) -> ArgsConfig[ContactAddIArgs]:
        return CONTACT_ADD_I_ARGS_CONFIG

    def _make_action(self, parsed_args: ContactAddIArgs) -> None:
        contact = Contact.model_validate(parsed_args.model_dump())

        contact_add(data_storage=self.data_storage, contact=contact)

        render_good_message(
            self.console,
            f"{Contact.get_meta_info().singular_name} '{contact.name}' added successfully.",
        )
