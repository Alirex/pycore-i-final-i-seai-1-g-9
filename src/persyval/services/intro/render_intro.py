from typing import TYPE_CHECKING

from rich.markup import escape
from rich.panel import Panel

from persyval.constants.app_info import APP_NAME
from persyval.services.commands.commands_enum import Command

if TYPE_CHECKING:
    from rich.console import Console


def render_intro(console: Console) -> None:
    msg_intro = f"""[yellow]Welcome to the personal assistant chat.

            .-------.
           / O     O \\
          |     |     |
           \\  \\___/  /
            `-------'

Type [bold]{escape(Command.HELP)}[/bold] for a list of available commands.
[italic]Autocomplete for commands is enabled.[/italic]

[italic]Press [bold]Enter[/bold] to access the selectable menu.[/italic][/yellow]"""

    app_name = APP_NAME.capitalize()

    panel = Panel(
        msg_intro,
        title=f"[bold]{escape(app_name)}[/bold]",
        title_align="left",
        border_style="bold blue",
        expand=False,
    )

    console.print(panel)
