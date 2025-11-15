from typing import TYPE_CHECKING, Any

from persyval.constants.text import CHOICE_I_TO_MAIN_MENU

if TYPE_CHECKING:
    from persyval.services.console.types import PromptToolkitFormattedText


def add_option_i_to_main_menu(
    options: list[tuple[Any | None, PromptToolkitFormattedText]],
) -> None:
    options.append((None, CHOICE_I_TO_MAIN_MENU))
