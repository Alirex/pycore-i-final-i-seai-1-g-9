from typing import TYPE_CHECKING

from pydantic import BaseModel
from rich.markup import escape
from rich.table import Table

from persyval.services.commands.commands_enum import COMMANDS_ORDER
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.services.handlers_base.helpers.no_direct_args_check import (
    no_direct_args_check,
)

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput


class HelpItem(BaseModel):
    command: str
    args: list[str]
    description: str


class HelpIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        no_direct_args_check(self.args)

        # ---------

        from persyval.services.commands.commands_meta_registry import (  # noqa: PLC0415
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

        # ---------

        table = Table(title="Available Commands", title_justify="left")
        table.add_column("Command", justify="left", style="cyan", no_wrap=True)
        table.add_column("Description", justify="left")

        for item in help_items:
            command_full = item.command
            if item.args:
                command_full += f" {[f'[{arg}]' for arg in item.args]}"

            table.add_row(
                escape(command_full),
                escape(item.description),
            )

        self.console.print(table)

        return None
