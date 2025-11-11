from typing import TypeAlias

from pydantic import BaseModel
from rich.table import Table

from goit_i_pycore_i_personal_assistant.exceptions.invalid_command_error import InvalidCommandError
from goit_i_pycore_i_personal_assistant.services.commands.commands_enum import COMMANDS_ORDER
from goit_i_pycore_i_personal_assistant.services.handlers_base.handler_base import HandlerBase
from goit_i_pycore_i_personal_assistant.services.handlers_base.handler_output import HandlerOutput


class HelpItem(BaseModel):
    command: str
    args: list[str]
    description: str


T_HELP_LIST: TypeAlias = list[HelpItem]


# noinspection PyTypeChecker
class HelpIHandler(HandlerBase[None, T_HELP_LIST]):
    def _parse_args(self) -> None:
        if self.args:
            msg = "Command does not take any arguments."
            raise InvalidCommandError(msg)

    def _make_action(
        self,
        parsed_args: None,  # noqa: ARG002
    ) -> T_HELP_LIST:
        from goit_i_pycore_i_personal_assistant.services.commands.commands_meta_registry import (  # noqa: PLC0415
            COMMANDS_META_REGISTRY,
        )

        help_items = []
        for command in COMMANDS_ORDER:
            command_meta = COMMANDS_META_REGISTRY[command]
            help_items.append(
                HelpItem(
                    command=str(command_meta.command),
                    args=command_meta.args,
                    description=command_meta.description,
                ),
            )

        return help_items

    def _get_or_render_output(
        self,
        output_data: T_HELP_LIST,
    ) -> HandlerOutput:
        table = Table(title="Available Commands")
        table.add_column("Command", justify="left", style="cyan", no_wrap=True)
        table.add_column("Arguments", justify="left", style="magenta")
        table.add_column("Description", justify="left")

        for item in output_data:
            table.add_row(item.command, ", ".join(item.args), item.description)

        self.console.print(table)

        return HandlerOutput()
