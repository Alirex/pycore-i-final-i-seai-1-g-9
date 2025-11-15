from typing import TYPE_CHECKING

from persyval.services.handlers.shared.args_i_empty import ARGS_CONFIG_I_EMPTY, ArgsIEmpty
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.format import render_good_message

if TYPE_CHECKING:
    from persyval.services.commands.args_config import ArgsConfig
    from persyval.services.handlers_base.handler_output import HandlerOutput


class HelloIHandler(
    HandlerBase[ArgsIEmpty],
):
    def _get_args_config(self) -> ArgsConfig[ArgsIEmpty]:
        return ARGS_CONFIG_I_EMPTY

    def _make_action(
        self,
        parsed_args: ArgsIEmpty,  # noqa: ARG002
    ) -> HandlerOutput | None:
        render_good_message(
            self.console,
            message="Hello, how can I assist you today?",
            title="Hello",
        )
        return None
