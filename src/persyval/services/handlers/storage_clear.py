from typing import TYPE_CHECKING

from persyval.services.commands.args_config import ArgMetaConfig, ArgsConfig, ArgType
from persyval.services.console.yes_no_dialog import yes_no_dialog
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message, render_good_message

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput


class StorageClearIForce(HandlerArgsBase):
    force: bool | None = None


STORAGE_CLEAR_I_ARGS_CONFIG = ArgsConfig[StorageClearIForce](
    result_cls=StorageClearIForce,
    args=[
        ArgMetaConfig(
            name="force",
            type_=ArgType.BOOL,
        ),
    ],
)


class StorageClearIHandler(
    HandlerBase[StorageClearIForce],
):
    def _get_args_config(self) -> ArgsConfig[StorageClearIForce]:
        return STORAGE_CLEAR_I_ARGS_CONFIG

    def _make_action(self, parsed_args: StorageClearIForce) -> HandlerOutput | None:
        if parsed_args.force is None:
            title = "Confirm Storage Clear"
            text = "Are you sure you want to clear the storage? This action cannot be undone."
            if self.terminal_simplified:
                message = f"{title}\n{text} (enter to confirm, any key to cancel)"
                is_do = not bool(input(message).strip())

            else:
                is_do = yes_no_dialog(
                    title=title,
                    text=text,
                )
        else:
            is_do = parsed_args.force

        if not is_do:
            render_canceled_message(
                console=self.console,
                message="Storage clear operation cancelled by user.",
            )
            return None

        # ---

        self.data_storage.clear()

        # ---

        message = "Storage cleared successfully."

        render_good_message(
            console=self.console,
            message=message,
        )

        return None
