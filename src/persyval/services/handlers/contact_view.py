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
        parse_result = CONTACT_VIEW_I_ARGS_CONFIG.parse(self.args)

        self._make_action(parse_result)

        return None

    def parsed_call(self, parse_result: ContactViewIArgs) -> None:
        self._make_action(parse_result)

    def _make_action(self, parse_result: ContactViewIArgs) -> None:
        # Get contact via data_action

        # Render all the fields of the contact. You can use rich, prompt_toolkit or something else.
        # But make it with colors.

        print(parse_result.uid)
