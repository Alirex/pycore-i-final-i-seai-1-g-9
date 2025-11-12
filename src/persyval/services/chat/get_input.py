from typing import TYPE_CHECKING

from persyval.services.console.completer import get_completer
from persyval.utils.format import format_prompt_message

if TYPE_CHECKING:
    from prompt_toolkit import PromptSession
    from rich.console import Console


def get_input(
    console: Console,
    prompt_session: PromptSession,  # type: ignore[type-arg]
) -> str:
    input_prompt_msg = format_prompt_message("Enter command: ")
    console.print(input_prompt_msg)

    result = prompt_session.prompt(
        message="> ",
        completer=get_completer(),
        show_frame=True,
    )

    return str(result)
