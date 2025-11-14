"""Formatting utils.

These functions are helpful for some simple standardized formatting of console messages.
"""

from typing import TYPE_CHECKING

from rich.markup import escape
from rich.panel import Panel

from persyval.services.console.types import RichFormattedText

if TYPE_CHECKING:
    from rich.console import Console

type T_MESSAGE_RAW = str

# TODO: (?) Use sometimes in-place colors (`console.print(msg, style=COLOR)` with constants?


def pack_colored_message(message: T_MESSAGE_RAW, color: str) -> RichFormattedText:
    return RichFormattedText(f"[{color}]{escape(message)}[/{color}]")


def format_repeated_message(message: T_MESSAGE_RAW) -> RichFormattedText:
    return pack_colored_message(message, "magenta")


def format_system_message(message: T_MESSAGE_RAW) -> RichFormattedText:
    return pack_colored_message(message, "yellow")


def format_prompt_message(message: T_MESSAGE_RAW) -> RichFormattedText:
    return pack_colored_message(message, "blue")


def format_good_message(message: T_MESSAGE_RAW) -> RichFormattedText:
    return pack_colored_message(message, "green")


def format_bad_message(message: T_MESSAGE_RAW) -> RichFormattedText:
    return pack_colored_message(message, "red")


def render_with_panel(
    console: Console,
    message: RichFormattedText,
    title: T_MESSAGE_RAW | None = None,
    style: str = "green",
) -> None:
    panel = Panel(
        message,
        title=f"{escape(title)}" if title else None,
        title_align="left",
        border_style=style,
        expand=False,
    )
    console.print(panel)


def render_good_message(
    console: Console,
    message: T_MESSAGE_RAW,
    title: T_MESSAGE_RAW | None = "Success",
) -> None:
    panel = Panel(
        escape(message),
        title=f"{escape(title)}" if title else None,
        title_align="left",
        border_style="green",
        expand=False,
    )
    console.print(panel)


def render_canceled_message(
    console: Console,
    message: T_MESSAGE_RAW,
    title: T_MESSAGE_RAW | None = "Canceled",
) -> None:
    panel = Panel(
        escape(message),
        title=f"{escape(title)}" if title else None,
        title_align="left",
        border_style="yellow",
        expand=False,
    )
    console.print(panel)


def render_error(
    console: Console,
    message: T_MESSAGE_RAW,
    title: T_MESSAGE_RAW | None = "Error",
) -> None:
    panel = Panel(
        escape(message),
        title=f"{escape(title)}" if title else None,
        title_align="left",
        border_style="red",
        expand=False,
    )
    console.print(panel)
