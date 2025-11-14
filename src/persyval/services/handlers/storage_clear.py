from typing import TYPE_CHECKING

from prompt_toolkit.shortcuts import yes_no_dialog

from persyval.services.handlers.shared.args_i_force import ARGS_CONFIG_I_FORCE, ArgsIForce
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_canceled_message, render_good_message

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput


STORAGE_CLEAR_I_ARGS_CONFIG = ARGS_CONFIG_I_FORCE


class StorageClearIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        parsed_args = STORAGE_CLEAR_I_ARGS_CONFIG.parse(self.args)
        self._make_action(parsed_args)
        return None

    def parsed_call(self, parsed_args: ArgsIForce) -> None:
        self._make_action(parsed_args)

    def _make_action(self, parsed_args: ArgsIForce) -> None:
        if parsed_args.force is None:
            is_do = yes_no_dialog(
                title="Confirm Storage Clear",
                text="Are you sure you want to clear the storage? This action cannot be undone.",
            ).run()
        else:
            is_do = parsed_args.force

        if not is_do:
            render_canceled_message(
                console=self.console,
                message="Storage clear operation cancelled by user.",
            )
            return

        # ---

        self.data_storage.clear()

        # ---

        message = "Storage cleared successfully."

        render_good_message(
            console=self.console,
            message=message,
        )
