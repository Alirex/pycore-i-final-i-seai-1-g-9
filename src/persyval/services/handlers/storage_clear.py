from typing import TYPE_CHECKING

from prompt_toolkit.shortcuts import yes_no_dialog

from persyval.services.handlers.shared.args_i_force import ARGS_CONFIG_I_FORCE
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message, render_good_message

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput


STORAGE_CLEAR_I_ARGS_CONFIG = ARGS_CONFIG_I_FORCE


class StorageClearIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        parse_result = STORAGE_CLEAR_I_ARGS_CONFIG.parse(self.args)

        if parse_result.force is None:
            is_do = yes_no_dialog(
                title="Confirm Storage Clear",
                text="Are you sure you want to clear the storage? This action cannot be undone.",
            ).run()
        else:
            is_do = parse_result.force

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
