from typing import TYPE_CHECKING

from prompt_toolkit import HTML, prompt

from persyval.models.contact import Contact, parse_birthday
from persyval.services.data_actions.contact_add import contact_add
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.services.handlers_base.helpers.no_direct_args_check import (
    no_direct_args_check,
)
from persyval.utils.format import render_good_message

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput


class ContactAddIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        # TODO: (?) Use optional direct args?
        no_direct_args_check(self.args)

        name = prompt(HTML("Enter <b>name</b>: "))
        address = prompt(HTML("Enter <b>address</b> <i>(Optional)</i>: ")) or None
        birthday = prompt(HTML("Enter <b>birthday</b> <i>(Optional)(YYYY-MM-DD)</i>: ")) or None

        contact = Contact(
            name=name,
            address=address,
            birthday=parse_birthday(birthday) if birthday else None,
        )

        contact_add(data_storage=self.data_storage, contact=contact)

        render_good_message(
            self.console,
            f"Contact '{contact.name}' added successfully.",
        )

        return None
