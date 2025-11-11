"""Formatting utils.

These functions are helpful for some simple standardized formatting of console messages.
"""

from rich.markup import escape

from persyval.services.console.types import RichFormattedText

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


def format_error(error: T_MESSAGE_RAW, message: T_MESSAGE_RAW) -> RichFormattedText:
    return RichFormattedText(f"{format_bad_message(error)}: {escape(message)}")
