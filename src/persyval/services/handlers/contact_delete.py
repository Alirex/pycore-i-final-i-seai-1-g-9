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


class ContactRemoveIArgs(BaseModel):
    uid: ContactUid
    force: bool | None = None


CONTACT_REMOVE_I_ARGS_CONFIG = ArgsConfig[ContactRemoveIArgs](
    result_cls=ContactRemoveIArgs,
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
        parse_result = CONTACT_REMOVE_I_ARGS_CONFIG.parse(self.args)

        if parse_result.force is None:
            is_do = yes_no_dialog(
                title="Confirm Contact Remove",
                text="Are you sure you want to remove the contact?",
            ).run()

        else:
            is_do = parse_result.force

        if not is_do:
            render_canceled_message(
                self.console,
                "Contact remove operation cancelled by user.",
            )
            return None

        contact_delete(data_storage=self.data_storage, contact_uid=parse_result.uid)

        render_good_message(
            self.console,
            f"Contact with uid {parse_result.uid} has been removed.",
        )

        return None
