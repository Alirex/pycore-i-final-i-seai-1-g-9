from typing import TYPE_CHECKING

from prompt_toolkit.shortcuts import yes_no_dialog
from pydantic import BaseModel

from persyval.models.contact import (
    ContactUid,
)
from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig, ArgType
from persyval.services.data_actions.contact_delete import contact_delete
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message, render_good_message

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput


class ContactDeleteIArgs(BaseModel):
    uid: ContactUid
    force: bool | None = None


CONTACT_DELETE_I_ARGS_CONFIG = ArgsConfig[ContactDeleteIArgs](
    result_cls=ContactDeleteIArgs,
    args=[
        ArgMetaConfig(
            name="uid",
            required=True,
        ),
        ArgMetaConfig(
            name="force",
            type_=ArgType.BOOL,
        ),
    ],
)


class ContactDeleteIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        parsed_args = CONTACT_DELETE_I_ARGS_CONFIG.parse(self.args)
        self._make_action(parsed_args)
        return None

    def parsed_call(self, parsed_args: ContactDeleteIArgs) -> None:
        self._make_action(parsed_args)

    def _make_action(self, parsed_args: ContactDeleteIArgs) -> None:
        if parsed_args.force is None:
            is_do = yes_no_dialog(
                title="Confirm Contact Remove",
                text="Are you sure you want to remove the contact?",
            ).run()

        else:
            is_do = parsed_args.force

        if not is_do:
            render_canceled_message(
                self.console,
                "Contact remove operation cancelled by user.",
            )
            return

        # ---

        contact = contact_delete(data_storage=self.data_storage, contact_uid=parsed_args.uid)

        render_good_message(
            self.console,
            f"Contact '{contact.name}' ({contact.uid}) has been deleted.",
        )

        return
