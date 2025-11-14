from typing import TYPE_CHECKING

from persyval.services.commands.commands_enum import COMMANDS_ORDER
from persyval.services.commands.commands_meta_registry import COMMANDS_META_REGISTRY

if TYPE_CHECKING:
    from collections.abc import Generator

    from persyval.services.commands.command_meta import CommandMeta


def iterate_over_commands_meta(*, show_hidden: bool = False) -> Generator[CommandMeta]:
    for command in COMMANDS_ORDER:
        command_meta = COMMANDS_META_REGISTRY[command]

        if not show_hidden and command_meta.hidden:
            continue

        yield command_meta
