from persyval.models.contact import (
    ContactUid,
)
from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.handlers_base.handler_base import HandlerBase


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
        # Get contact via data_action

        # Render all the fields of the contact. You can use rich, prompt_toolkit or something else.
        # But make it with colors.

        print(parsed_args.uid)
