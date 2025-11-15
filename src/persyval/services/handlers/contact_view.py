from typing import TYPE_CHECKING

from persyval.models.contact import (
    Contact,
    ContactUid,
)
from persyval.services.birthday.parse_and_format import format_birthday_for_output
from persyval.services.commands.args_config import ArgMetaConfig, ArgsConfig
from persyval.services.console.render_item_card_with_panel import RenderItem, render_item_card_with_panel
from persyval.services.data_actions.contact_get import contact_get
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.handlers.contacts.contact_item_ask_next_action import contact_item_ask_next_action
from persyval.services.handlers_base.handler_base import HandlerBase

if TYPE_CHECKING:
    from rich.console import Console


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
        uid = parsed_args.uid

        contact = contact_get(
            data_storage=self.data_storage,
            uid=uid,
        )

        render_details(
            console=self.console,
            contact=contact,
        )

        if self.non_interactive:
            return

        contact_item_ask_next_action(
            execution_queue=self.execution_queue,
            uid=uid,
            is_from_view=True,
        )


def render_details(console: Console, contact: Contact) -> None:
    render_item_card_with_panel(
        console=console,
        entity_title=contact.get_meta_info().singular_name,
        list_to_render=[
            RenderItem(name="Name", value=contact.name),
            RenderItem(name="Address", value=contact.address),
            RenderItem(
                name="Birthday",
                value=format_birthday_for_output(contact.birthday) if contact.birthday else None,
            ),
            RenderItem(name="Phones", value=", ".join(contact.phones) if contact.phones else None),
            RenderItem(name="Emails", value=", ".join(contact.emails) if contact.emails else None),
            RenderItem(name="Uid", value=str(contact.uid)),
        ],
    )
