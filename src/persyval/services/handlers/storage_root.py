import enum
from typing import TYPE_CHECKING

from prompt_toolkit import choice

from persyval.services.commands.args_config import ArgMetaConfig, ArgsConfig
from persyval.services.commands.commands_enum import Command
from persyval.services.execution_queue.execution_queue import (
    HandlerArgsBase,
    HandlerFullArgs,
)
from persyval.services.handlers.shared.args_i_empty import ArgsIEmpty
from persyval.services.handlers_base.handler_base import HandlerBase

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput


@enum.unique
class StorageRootIAction(enum.StrEnum):
    CLEAR = "clear"
    STATS = "stats"


class StorageRootIArgs(HandlerArgsBase):
    action: StorageRootIAction | None = None


STORAGE_ROOT_I_ARGS_CONFIG = ArgsConfig[StorageRootIArgs](
    result_cls=StorageRootIArgs,
    args=[
        ArgMetaConfig(
            name="action",
        ),
    ],
)


class StorageRootIHandler(
    HandlerBase[StorageRootIArgs],
):
    def _get_args_config(self) -> ArgsConfig[StorageRootIArgs]:
        return STORAGE_ROOT_I_ARGS_CONFIG

    def _make_action(self, parsed_args: StorageRootIArgs) -> HandlerOutput | None:
        if parsed_args.action is not None:
            choice_result = parsed_args.action
        else:
            choice_result = choice(
                message="Choose action:",
                options=[(item, str(item).capitalize()) for item in StorageRootIAction],
            )

        match choice_result:
            # TODO: (?) Use lazy import, when available. https://peps.python.org/pep-0810/
            case StorageRootIAction.CLEAR:
                from persyval.services.handlers.storage_clear import StorageClearIForce  # noqa: PLC0415

                self.execution_queue.put(
                    HandlerFullArgs(
                        command=Command.STORAGE_CLEAR,
                        args=StorageClearIForce(),
                    ),
                )
            case StorageRootIAction.STATS:
                self.execution_queue.put(
                    HandlerFullArgs(
                        command=Command.STORAGE_STATS,
                        args=ArgsIEmpty(),
                    ),
                )

        return None
