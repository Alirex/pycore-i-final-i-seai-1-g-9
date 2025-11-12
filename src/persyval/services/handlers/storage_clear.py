from typing import TYPE_CHECKING

from prompt_toolkit.shortcuts import yes_no_dialog

from persyval.exceptions.main import InvalidCommandError
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.convert_command_part_to_bool import convert_command_part_to_bool
from persyval.utils.format import render_canceled_message, render_good_message

if TYPE_CHECKING:
    from persyval.services.handlers_base.handler_output import HandlerOutput


class StorageClearIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        if len(self.args) > 1:
            msg = "Invalid number of arguments."
            raise InvalidCommandError(msg)

        is_force = convert_command_part_to_bool(self.args[0]) if self.args else None

        if is_force is None:
            is_force = yes_no_dialog(
                title="Confirm Storage Clear",
                text="Are you sure you want to clear the storage? This action cannot be undone.",
            ).run()

        if not is_force:
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
