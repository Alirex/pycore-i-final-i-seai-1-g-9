from prompt_toolkit.shortcuts import yes_no_dialog

from persyval.services.handlers.shared.args_i_force import ARGS_CONFIG_I_FORCE
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.services.handlers_base.handler_output import HandlerOutput
from persyval.utils.format import render_canceled_message, render_good_message

EXIT_I_ARGS_CONFIG = ARGS_CONFIG_I_FORCE


class ExitIHandler(
    HandlerBase,
):
    def _handler(self) -> HandlerOutput | None:
        parsed_args = EXIT_I_ARGS_CONFIG.parse(self.args)

        if parsed_args.force is None:
            is_do = yes_no_dialog(
                title="Exit",
                text="Are you sure you want to exit?",
            ).run()
        else:
            is_do = parsed_args.force

        if not is_do:
            render_canceled_message(
                self.console,
                "I'm glad that you decided to stay with me.",
            )
            return None

        render_good_message(self.console, "Goodbye!", "Exit")
        return HandlerOutput(is_exit=True)
