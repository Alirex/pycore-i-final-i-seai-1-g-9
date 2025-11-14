from typing import TYPE_CHECKING

from pydantic import BaseModel

from persyval.models.contact import (
    ContactUid,
)
from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig
from persyval.services.handlers_base.handler_base import HandlerBase

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput


class ContactViewIArgs(BaseModel):
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
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        parsed_args = CONTACT_VIEW_I_ARGS_CONFIG.parse(self.args)

        self._make_action(parsed_args)

        return None

    def parsed_call(self, parsed_args: ContactViewIArgs) -> None:
        self._make_action(parsed_args)

    def _make_action(self, parsed_args: ContactViewIArgs) -> None:
        # Get contact via data_action

        # Render all the fields of the contact. You can use rich, prompt_toolkit or something else.
        # But make it with colors.

        print(parsed_args.uid)
