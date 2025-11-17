from typing import TYPE_CHECKING, Any

from persyval.services.console.completer import get_completer
from persyval.utils.format import format_prompt_message

if TYPE_CHECKING:
    from prompt_toolkit import PromptSession
    from rich.console import Console


def get_input(
    *,
    console: Console,
    prompt_session: PromptSession[Any] | None,
    use_advanced_completer: bool = False,
) -> str:
    input_prompt_msg = format_prompt_message("Enter command: ")
    console.print(input_prompt_msg)

    if prompt_session:
        result = str(
            prompt_session.prompt(  # pyright: ignore[reportUnknownArgumentType]
                message="> ",
                completer=get_completer(use_advanced_completer=use_advanced_completer),
                show_frame=True,
            ),
        )
    else:
        result = input("> ")

    return str(result)
