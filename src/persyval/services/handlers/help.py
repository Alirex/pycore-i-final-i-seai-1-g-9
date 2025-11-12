from typing import TYPE_CHECKING

from rich.markup import escape
from rich.table import Table

from persyval.services.commands.command_meta import ArgMetaConfig
from persyval.services.commands.commands_enum import COMMANDS_ORDER
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.services.handlers_base.helpers.no_direct_args_check import (
    no_direct_args_check,
)

if TYPE_CHECKING:
    from rich.console import Console

    from persyval.services.handlers_base.handler_output import HandlerOutput


class HelpIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        no_direct_args_check(self.args)

        # ---------

        render_help(console=self.console)

        return None


def render_help(
    console: Console,
) -> None:
    from persyval.services.commands.commands_meta_registry import (  # noqa: PLC0415
        COMMANDS_META_REGISTRY,
    )

    # Note: Moved from handler because it is relatively clear.

    table = Table(title="Available Commands", title_justify="left")
    table.add_column("Command", justify="left", style="cyan", no_wrap=True)
    table.add_column("Description", justify="left")

    for command in COMMANDS_ORDER:
        command_meta = COMMANDS_META_REGISTRY[command]

        command_full = str(command_meta.command)
        if command_meta.args_config:
            args: list[str] = []
            for arg in command_meta.args_config.args:
                arg_obj = ArgMetaConfig(name=arg, required=False) if isinstance(arg, str) else arg

                is_required_char = "*" if arg_obj.required else "?"

                arg_type_as_str = str(arg_obj.type_)

                arg_str = (
                    f"[[bold]{escape(is_required_char)}[/bold]"
                    f"{escape(arg_obj.name)}"
                    f":[italic]{escape(arg_type_as_str)}[/italic]]"
                )
                args.append(arg_str)

            command_full += f" {' '.join(args)}"

        table.add_row(
            command_full,
            escape(command_meta.description),
        )

    console.print(table)
