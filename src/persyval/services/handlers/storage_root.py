import enum
from typing import TYPE_CHECKING

from prompt_toolkit import choice
from pydantic import BaseModel

from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig
from persyval.services.handlers_base.handler_base import HandlerBase

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput


@enum.unique
class StorageRootIAction(enum.StrEnum):
    CLEAR = "clear"
    STATS = "stats"


class StorageRootIArgs(BaseModel):
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
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        parsed_args = STORAGE_ROOT_I_ARGS_CONFIG.parse(self.args)
        self._make_action(parsed_args)
        return None

    def parsed_call(self, parsed_args: StorageRootIArgs) -> None:
        self._make_action(parsed_args)

    def _make_action(self, parsed_args: StorageRootIArgs) -> None:
        if parsed_args.action is not None:
            choice_result = parsed_args.action
        else:
            choice_result = choice(
                message="Choose action:",
                options=[(item, str(item).capitalize()) for item in StorageRootIAction],
            )

        match choice_result:
            case StorageRootIAction.CLEAR:
                from persyval.services.handlers.storage_clear import (  # noqa: PLC0415
                    STORAGE_CLEAR_I_ARGS_CONFIG,
                    StorageClearIHandler,
                )

                StorageClearIHandler(
                    **(self.model_dump() | {"args": []}),
                ).parsed_call(
                    STORAGE_CLEAR_I_ARGS_CONFIG.parse([]),
                )
            case StorageRootIAction.STATS:
                from persyval.services.handlers.storage_stats import (  # noqa: PLC0415
                    StorageStatsIHandler,
                )

                StorageStatsIHandler(
                    **(self.model_dump() | {"args": []}),
                ).parsed_call(
                    None,
                )
