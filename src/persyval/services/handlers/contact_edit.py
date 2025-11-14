import copy
from typing import TYPE_CHECKING

from prompt_toolkit import HTML, prompt

from persyval.services.birthday.parse_and_format import (
    format_birthday_for_edit,
    parse_birthday,
)
from persyval.services.birthday.validate_birthday import validate_birthday
from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig
from persyval.services.data_actions.contact_get import contact_get
from persyval.services.data_actions.contact_update import contact_update
from persyval.services.email.validate_email import parse_emails, validate_email_list
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.services.phone.validate_phone_list import (
    parse_phones,
    validate_phone_list,
)
from persyval.utils.format import render_good_message

if TYPE_CHECKING:
    from persyval.models.contact import (
        ContactUid,
    )
    from persyval.services.handlers_base.handler_output import HandlerOutput


class ContactEditIArgs(HandlerArgsBase):
    uid: ContactUid
    force: bool | None = None


CONTACT_EDIT_I_ARGS_CONFIG = ArgsConfig[ContactEditIArgs](
    result_cls=ContactEditIArgs,
    args=[
        ArgMetaConfig(
            name="uid",
            required=True,
        ),
    ],
)


class ContactEditIHandler(
    HandlerBase[ContactEditIArgs],
):
    def _get_args_config(self) -> ArgsConfig[ContactEditIArgs]:
        return CONTACT_EDIT_I_ARGS_CONFIG

    def _make_action(self, parsed_args: ContactEditIArgs) -> HandlerOutput | None:
        contact = copy.deepcopy(
            contact_get(
                data_storage=self.data_storage,
                contact_uid=parsed_args.uid,
            ),
        )

        name = prompt(
            message=HTML("<b>Name</b>: "),
            default=str(contact.name),
        )
        address = prompt(
            message=HTML("<b>Address</b>: "),
            default=str(contact.address) if contact.address else "",
        )
        birthday = prompt(
            message=HTML("<b>Birthday</b> (YYYY-MM-DD): "),
            default=format_birthday_for_edit(contact.birthday) if contact.birthday else "",
        )

        phones_input = prompt(
            message=HTML("<b>Phones</b>: "),
            default=",".join(contact.phones) if contact.phones else "",
        )

        phones_list = parse_phones(phones_input)

        emails_input = prompt(
            message=HTML("<b>Emails</b>: "),
            default=",".join(contact.emails) if contact.emails else "",
        )

        emails_list = parse_emails(emails_input)

        contact.name = name
        contact.address = address
        contact.birthday = validate_birthday(parse_birthday(birthday)) if birthday else None
        contact.phones = validate_phone_list(phones_list)
        contact.emails = validate_email_list(emails_list)

        contact = contact_update(
            data_storage=self.data_storage,
            contact=contact,
        )

        render_good_message(
            self.console,
            f"Contact '{contact.name}' edited successfully.",
        )

        return None
