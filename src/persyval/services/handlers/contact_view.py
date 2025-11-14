from persyval.models.contact import (
    ContactUid,
)
from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig
from persyval.services.data_actions.contact_get import contact_get
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_good_message


class ContactViewIArgs(HandlerArgsBase):
    uid: ContactUid


CONTACT_VIEW_I_ARGS_CONFIG = ArgsConfig[ContactViewIArgs](
    result_cls=ContactViewIArgs,
    args=[
        ArgMetaConfig(
            name="uid",
            required=True,
        ),
    ],
)


class ContactViewIHandler(
    HandlerBase[ContactViewIArgs],
):
    def _get_args_config(self) -> ArgsConfig[ContactViewIArgs]:
        return CONTACT_VIEW_I_ARGS_CONFIG

    def _make_action(self, parsed_args: ContactViewIArgs) -> None:
        contact_uid = parsed_args.uid

        contact = contact_get(
            data_storage=self.data_storage,
            contact_uid=contact_uid,
        )

        phones = ", ".join(contact.phones) if contact.phones else "-"
        emails = ", ".join(contact.emails) if contact.emails else "-"
        address = contact.address or "-"
        birthday = contact.birthday.isoformat() if contact.birthday else "-"
        message = (
            "Contact details\n"
            f"Name: {contact.name}\n"
            f"Address: {address}\n"
            f"Birthday: {birthday}\n"
            f"Phones: {phones}\n"
            f"Emails: {emails}"
        )

        render_good_message(self.console, message)
