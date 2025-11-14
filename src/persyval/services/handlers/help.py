from typing import TYPE_CHECKING

from rich.markup import escape
from rich.table import Table

from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig, ArgType
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.handlers_base.handler_base import HandlerBase

if TYPE_CHECKING:
    from rich.console import Console


class HelpIArgs(HandlerArgsBase):
    advanced: bool = False


HELP_I_ARGS_CONFIG = ArgsConfig[HelpIArgs](
    result_cls=HelpIArgs,
    args=[
        ArgMetaConfig(
            name="advanced",
            type_=ArgType.BOOL,
        ),
    ],
)


class HelpIHandler(
    HandlerBase[HelpIArgs],
):
    def _get_args_config(self) -> ArgsConfig[HelpIArgs]:
        return HELP_I_ARGS_CONFIG

    def _make_action(self, parsed_args: HelpIArgs) -> None:
        render_help(console=self.console, show_hidden=parsed_args.advanced)


def render_help(
    *,
    console: Console,
    show_hidden: bool = False,
) -> None:
    # Note: Moved from handler because it is relatively clear.

    table = Table(title="Available Commands", title_justify="left")
    table.add_column("Command", justify="left", style="cyan", no_wrap=True)
    table.add_column("Description", justify="left")

    from persyval.services.commands.iterate_over_commands_meta import iterate_over_commands_meta  # noqa: PLC0415

    for command_meta in iterate_over_commands_meta(show_hidden=show_hidden):
        command_full = str(command_meta.command)
        if command_meta.args_config:
            args: list[str] = []
            for arg in command_meta.args_config.args:
                arg_obj = ArgMetaConfig(name=arg, required=False) if isinstance(arg, str) else arg

                is_required_char = "*" if arg_obj.required else "?"

                arg_type_as_str = str(arg_obj.type_)

                arg_str = (
                    "["
                    f"[bold]{escape(is_required_char)}[/bold]"
                    f"{escape(arg_obj.name)}"
                    f":[italic]{escape(arg_type_as_str)}[/italic]"
                    f"{f'({escape(arg_obj.format)})' if arg_obj.format else ''}"
                    "]"
                )
                args.append(arg_str)

            command_full += f" {' '.join(args)}"

        table.add_row(
            command_full,
            escape(command_meta.description),
        )

    console.print(table)
