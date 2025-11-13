import enum
from typing import TYPE_CHECKING

from persyval.exceptions.main import InvalidCommandError
from persyval.services.commands.commands_meta_registry import COMMANDS_META_REGISTRY
from persyval.services.parse_input.parse_input import parse_input
from persyval.utils.format import render_error

if TYPE_CHECKING:
    from rich.console import Console

    from persyval.services.data_storage.data_storage import DataStorage


@enum.unique
class LoopAction(enum.StrEnum):
    EXIT = "exit"
    CONTINUE = "continue"


def parse_input_and_make_action(  # noqa: PLR0913
    *,
    console: Console,
    data_storage: DataStorage,
    #
    user_input: str,
    show_commands: bool = False,
    #
    non_interactive: bool = False,
    plain_render: bool = False,
    terminal_simplified: bool = False,
) -> LoopAction:
    try:
        parsed_input = parse_input(user_input)
    except InvalidCommandError as exc:
        render_error(
            console=console,
            message=str(exc),
            title="Invalid Command",
        )
        return LoopAction.CONTINUE

    if show_commands:
        console.print(parsed_input.get_rich_cli())

    command_meta = COMMANDS_META_REGISTRY[parsed_input.command]

    handler_obj = command_meta.handler(
        args=parsed_input.args,
        #
        data_storage=data_storage,
        console=console,
        #
        non_interactive=non_interactive,
        plain_render=plain_render,
        terminal_simplified=terminal_simplified,
    )
    handler_output = handler_obj.run()

    if handler_output is not None:
        if handler_output.message_rich:
            console.print(handler_output.message_rich)

        if handler_output.is_exit:
            return LoopAction.EXIT

    return LoopAction.CONTINUE
