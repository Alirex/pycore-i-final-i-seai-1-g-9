from prompt_toolkit.shortcuts import yes_no_dialog

from persyval.services.commands.command_meta import ArgMetaConfig, ArgsConfig, ArgType
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.services.handlers_base.handler_output import HandlerOutput
from persyval.utils.format import render_canceled_message, render_good_message


class ExitIForce(HandlerArgsBase):
    force: bool | None = None


EXIT_I_ARGS_CONFIG = ArgsConfig[ExitIForce](
    result_cls=ExitIForce,
    args=[
        ArgMetaConfig(
            name="force",
            type_=ArgType.BOOL,
        ),
    ],
)


class ExitIHandler(
    HandlerBase[ExitIForce],
):
    def _get_args_config(self) -> ArgsConfig[ExitIForce]:
        return EXIT_I_ARGS_CONFIG

    def _make_action(self, parsed_args: ExitIForce) -> HandlerOutput | None:
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
