from typing import TypeAlias

from pydantic import BaseModel, Field
from rich.markup import escape

from persyval.exceptions.main import InvalidCommandError
from persyval.services.commands.commands_enum import Command
from persyval.services.console.types import RichFormattedText

T_COMMAND: TypeAlias = str
T_ARGS: TypeAlias = list[str]


class UserInput(BaseModel):
    command: Command
    args: T_ARGS = Field(
        default_factory=list,
        description="List of arguments for the command.",
    )

    def get_rich_cli(self) -> RichFormattedText:
        msg = f"[bold]{escape(self.command)}[/bold]"
        if self.args:
            args = [f"'[italic]{escape(arg)}[/italic]'" for arg in self.args]
            msg += f" {' '.join(args)}"

        return RichFormattedText(msg)


def parse_input(user_input: str) -> UserInput:
    _parts = user_input.strip().split()

    try:
        command = Command(_parts.pop(0)) if _parts else Command.get_default()
    except ValueError as exc:
        msg = f"{user_input}"
        raise InvalidCommandError(msg) from exc

    args = _parts
    return UserInput(command=command, args=args)
