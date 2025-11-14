from typing import TYPE_CHECKING, Final

from pydantic import BaseModel
from rich.markup import escape

from persyval.models.contact import (
    Contact,
    ContactUid,
)
from persyval.services.birthday.parse_and_format import format_birthday_for_output
from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig
from persyval.services.console.types import RichFormattedText
from persyval.services.data_actions.contact_get import contact_get
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_with_panel

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
        contact_uid = parsed_args.uid

        contact = contact_get(
            data_storage=self.data_storage,
            contact_uid=contact_uid,
        )

        contact_render_details(
            console=self.console,
            contact=contact,
        )


class RenderItem(BaseModel):
    name: str
    value: str


RENDER_I_PLACEHOLDER: Final[str] = "-"
RENDER_I_STYLE: Final[str] = "green bold"


def contact_render_details(console: Console, contact: Contact) -> None:
    list_to_render: list[RenderItem] = [
        RenderItem(name="Name", value=contact.name),
        RenderItem(name="Address", value=contact.address or RENDER_I_PLACEHOLDER),
        RenderItem(
            name="Birthday",
            value=format_birthday_for_output(contact.birthday) if contact.birthday else RENDER_I_PLACEHOLDER,
        ),
        RenderItem(name="Phones", value=", ".join(contact.phones) if contact.phones else RENDER_I_PLACEHOLDER),
        RenderItem(name="Emails", value=", ".join(contact.emails) if contact.emails else RENDER_I_PLACEHOLDER),
        RenderItem(name="Uid", value=str(contact.uid)),
    ]

    message = "\n".join(
        [f"[{RENDER_I_STYLE}]{escape(item.name)}:[/{RENDER_I_STYLE}] {escape(item.value)}" for item in list_to_render],
    )

    render_with_panel(
        console=console,
        title="Contact details",
        message=RichFormattedText(message),
        style=RENDER_I_STYLE,
    )
