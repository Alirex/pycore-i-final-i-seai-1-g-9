from collections.abc import Sequence

from pydantic import BaseModel, Field
from rich.markup import escape

from persyval.exceptions.main import InvalidCommandError
from persyval.services.commands.commands_enum import Command
from persyval.services.console.types import RichFormattedText

type T_COMMAND = str
type T_ARGS = Sequence[str | None]


class UserInput(BaseModel):
    command: Command
    args: T_ARGS = Field(
        default_factory=list,
        description="List of arguments for the command.",
    )

    def get_rich_cli(self) -> RichFormattedText:
        msg = f"[bold]{escape(self.command)}[/bold]"
        if self.args:
            # args = [f"'[italic]{escape(arg)}[/italic]'" for arg in self.args]
            args = []
            for arg in self.args:
                arg_normalized = str(arg) if arg else None

                part = f"[italic]{escape(arg_normalized)}[/italic]" if arg_normalized else ""
                part = f"'{part}'"
                args.append(part)

            msg += f" {' '.join(args)}"

        return RichFormattedText(msg)


def parse_input(user_input: str) -> UserInput:
    # TODO: Implement advanced split. Split with regards to quotes (", '). For better multiword input.

    _parts = user_input.strip().split()

    try:
        command = Command(_parts.pop(0)) if _parts else Command.get_default()
    except ValueError as exc:
        msg = f"{user_input}"
        raise InvalidCommandError(msg) from exc

    args = _parts
    return UserInput(command=command, args=args)
