from typing import TYPE_CHECKING, Any

from prompt_toolkit import choice, print_formatted_text

from persyval.services.console.add_option_i_to_main_menu import add_option_i_to_main_menu
from persyval.services.model_meta.model_meta_info import ModelProtocol
from persyval.utils.format import render_canceled_message

if TYPE_CHECKING:
    from collections.abc import Callable

    from rich.console import Console

    from persyval.services.console.types import PromptToolkitFormattedText
    from persyval.services.data_storage.data_storage import DataStorage
    from persyval.services.execution_queue.execution_queue import ExecutionQueue
    from persyval.services.handlers.shared.sort_and_filter import ListConfig


def list_show[Uid, T: ModelProtocol[Any]](  # noqa: PLR0913
    *,
    list_config: ListConfig,
    data_storage: DataStorage,
    list_callable: Callable[[DataStorage, ListConfig], list[T]],
    next_action: Callable[[ExecutionQueue, Uid], None],
    #
    model: type[T],
    console: Console,
    execution_queue: ExecutionQueue,
    #
    plain_render: bool = False,
    non_interactive: bool = False,
) -> None:
    items = list_callable(
        data_storage,
        list_config,
    )

    if plain_render:
        for item in items:
            print(item.uid)
        return

    if non_interactive:
        for item in items:
            print_formatted_text(item.get_prompt_toolkit_output())

        return

    if not items:
        render_canceled_message(
            console,
            f"No {model.get_meta_info().plural_name.lower()} found.",
            title="Not found",
        )
        return

    options_list: list[tuple[Uid | None, PromptToolkitFormattedText]] = []
    add_option_i_to_main_menu(options_list)

    options_list.extend([(item.uid, item.get_prompt_toolkit_output()) for item in items])  # pyright: ignore[reportArgumentType]

    message_after_filter = f"{model.get_meta_info().plural_name} found: {len(items)}. \nChoose one to interact:"
    choice_by_list = choice(
        message=message_after_filter,
        options=options_list,
    )

    if choice_by_list is None:
        return

    next_action(
        execution_queue,
        choice_by_list,
    )

    return
