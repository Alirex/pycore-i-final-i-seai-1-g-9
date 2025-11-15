import enum
from typing import TYPE_CHECKING

from prompt_toolkit import choice

from persyval.services.commands.args_config import ArgMetaConfig, ArgsConfig
from persyval.services.commands.commands_enum import Command
from persyval.services.console.add_option_i_to_main_menu import (
    add_option_i_to_main_menu,
)
from persyval.services.execution_queue.execution_queue import (
    HandlerArgsBase,
    HandlerFullArgs,
)
from persyval.services.handlers.shared.args_i_empty import ArgsIEmpty
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.convert_snake_case_to_human_readable import (
    convert_snake_case_to_human_readable,
)

if TYPE_CHECKING:
    from persyval.services.console.types import PromptToolkitFormattedText


@enum.unique
class NotesRootIAction(enum.StrEnum):
    LIST = "list"
    ADD = "add"


class NotesRootIArgs(HandlerArgsBase):
    action: NotesRootIAction | None = None


NOTES_ROOT_I_ARGS_CONFIG = ArgsConfig[NotesRootIArgs](
    result_cls=NotesRootIArgs,
    args=[
        ArgMetaConfig(
            name="action",
        ),
    ],
)


class NotesRootIHandler(
    HandlerBase[NotesRootIArgs],
):
    def _get_args_config(self) -> ArgsConfig[NotesRootIArgs]:
        return NOTES_ROOT_I_ARGS_CONFIG

    def _make_action(self, parsed_args: NotesRootIArgs) -> None:
        choice_result: NotesRootIAction | None

        if parsed_args.action is not None:
            choice_result = parsed_args.action
        else:
            options: list[tuple[NotesRootIAction | None, PromptToolkitFormattedText]] = [
                (item, convert_snake_case_to_human_readable(item)) for item in NotesRootIAction
            ]
            add_option_i_to_main_menu(options)
            choice_result = choice(
                message="Choose action:",
                options=options,
            )

        if choice_result is None:
            return

        match choice_result:
            # TODO: (?) Use lazy import, when available. https://peps.python.org/pep-0810/
            case NotesRootIAction.LIST:
                from persyval.services.handlers.notes_list import NotesListIArgs  # noqa: PLC0415

                self.execution_queue.put(
                    HandlerFullArgs(
                        command=Command.NOTES_LIST,
                        args=NotesListIArgs(),
                    ),
                )

            case NotesRootIAction.ADD:
                self.execution_queue.put(
                    HandlerFullArgs(
                        command=Command.NOTE_ADD,
                        args=ArgsIEmpty(),
                    ),
                )
