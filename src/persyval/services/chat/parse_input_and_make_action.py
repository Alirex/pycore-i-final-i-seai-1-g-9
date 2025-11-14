import enum
import sys
from typing import TYPE_CHECKING

from persyval.exceptions.main import InvalidCommandError
from persyval.services.commands.commands_meta_registry import COMMANDS_META_REGISTRY
from persyval.services.parse_input.parse_input import parse_input
from persyval.utils.format import render_error

if TYPE_CHECKING:
    from rich.console import Console

    from persyval.services.data_storage.data_storage import DataStorage
    from persyval.services.execution_queue.execution_queue import ExecutionQueue


@enum.unique
class LoopAction(enum.StrEnum):
    EXIT = "exit"
    CONTINUE = "continue"


def parse_input_and_make_action(  # noqa: PLR0913
    *,
    console: Console,
    data_storage: DataStorage,
    #
    execution_queue: ExecutionQueue,
    show_commands: bool = False,
    #
    non_interactive: bool = False,
    plain_render: bool = False,
    terminal_simplified: bool = False,
    raise_sys_exit_on_error: bool = False,
    throw_full_error: bool = False,
) -> LoopAction:
    user_input = execution_queue.get()
    if isinstance(user_input, str):
        try:
            parsed_input = parse_input(user_input)
        except InvalidCommandError as exc:
            render_error(
                console=console,
                message=str(exc),
                title=exc.__class__.__name__,
            )

            if throw_full_error:
                raise

            if raise_sys_exit_on_error:
                sys.exit(1)

            return LoopAction.CONTINUE

        if show_commands:
            console.print(parsed_input.get_rich_cli())

        command = parsed_input.command
        args = parsed_input.args
        parsed_args = None
    else:
        command = user_input.command
        args = None
        parsed_args = user_input.args

    command_meta = COMMANDS_META_REGISTRY[command]

    handler_obj = command_meta.handler(
        execution_queue=execution_queue,
        #
        data_storage=data_storage,
        console=console,
        #
        non_interactive=non_interactive,
        plain_render=plain_render,
        terminal_simplified=terminal_simplified,
        raise_sys_exit_on_error=raise_sys_exit_on_error,
        throw_full_error=throw_full_error,
    )

    handler_output = handler_obj.run(
        args=args,
        parsed_args=parsed_args,
    )

    if handler_output is not None:
        if handler_output.message_rich:
            console.print(handler_output.message_rich)

        if handler_output.is_exit:
            return LoopAction.EXIT

    return LoopAction.CONTINUE
