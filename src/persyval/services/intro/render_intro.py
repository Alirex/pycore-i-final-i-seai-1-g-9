from typing import TYPE_CHECKING

from rich.markup import escape
from rich.panel import Panel

from persyval.constants.app_info import APP_NAME
from persyval.services.commands.commands_enum import Command

if TYPE_CHECKING:
    from rich.console import Console


def render_intro(console: Console) -> None:
    msg_intro = rf"""
    [cyan]
    ╭─────────────────────────────────────────────╮
    │        Welcome to your Assistant!           │
    ╰─────────────────────────────────────────────╯

            (\_/)
            ( •_•)   I'm here to help.
           / >💾     Just tell me what you need!

     Type [bold]{escape(Command.HELP)}[/bold] for available commands.
     Autocomplete is enabled.

     Press [bold]Enter[/bold] to open the menu.
    [/cyan]
    """
    app_name = APP_NAME.capitalize()

    panel = Panel(
        msg_intro,
        title=f"[bold]{escape(app_name)}[/bold]",
        title_align="left",
        border_style="bold blue",
        expand=False,
    )

    console.print(panel)
