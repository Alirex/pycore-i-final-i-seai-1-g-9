from typing import TYPE_CHECKING

from persyval.exceptions.main import InvalidCommandError

if TYPE_CHECKING:
    from persyval.services.parse_input.parse_input import T_ARGS


def no_direct_args_check(args: T_ARGS) -> None:
    if args:
        msg = "Command does not take any arguments."
        raise InvalidCommandError(msg)
