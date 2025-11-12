from prompt_toolkit.shortcuts import yes_no_dialog

from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.services.handlers_base.handler_output import HandlerOutput
from persyval.services.handlers_base.helpers.no_direct_args_check import (
    no_direct_args_check,
)
from persyval.utils.format import render_good_message


class ExitIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        no_direct_args_check(self.args)

        if yes_no_dialog(
            title="Exit",
            text="Are you sure you want to exit?",
        ).run():
            render_good_message(self.console, "Goodbye!", "Exit")
            return HandlerOutput(is_exit=True)

        render_good_message(
            self.console,
            "I'm glad that you decided to stay with me.",
            "Exit disabled",
        )

        return None
