from typing import TYPE_CHECKING

from prompt_toolkit import HTML, choice

from persyval.services.console.add_option_i_to_main_menu import (
    add_option_i_to_main_menu,
)
from persyval.services.handlers.shared.args_i_empty import (
    ARGS_CONFIG_I_EMPTY,
    ArgsIEmpty,
)
from persyval.services.handlers_base.handler_base import HandlerBase

if TYPE_CHECKING:
    from persyval.services.commands.args_config import ArgsConfig
    from persyval.services.commands.commands_enum import Command
    from persyval.services.console.types import PromptToolkitFormattedText


class RootIHandler(
    HandlerBase[ArgsIEmpty],
):
    def _get_args_config(self) -> ArgsConfig[ArgsIEmpty]:
        return ARGS_CONFIG_I_EMPTY

    def _make_action(
        self,
        parsed_args: ArgsIEmpty,  # noqa: ARG002
    ) -> None:
        options: list[tuple[Command | None, PromptToolkitFormattedText]] = []

        from persyval.services.commands.iterate_over_commands_meta import (  # noqa: PLC0415
            iterate_over_commands_meta,
        )

        for command_meta in iterate_over_commands_meta():
            text = f"<b>{command_meta.command}</b>"
            if command_meta.description:
                text += f" - <i>{command_meta.description}</i>"
            options.append((command_meta.command, HTML(text)))

        add_option_i_to_main_menu(options)

        selected = choice(
            message="Select a command:",
            options=options,
        )

        if selected is None:
            return

        self.execution_queue.put(str(selected))
