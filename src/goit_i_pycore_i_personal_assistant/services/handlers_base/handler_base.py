import abc

import rich
from pydantic import BaseModel, ConfigDict

from goit_i_pycore_i_personal_assistant.exceptions.invalid_command_error import InvalidCommandError
from goit_i_pycore_i_personal_assistant.services.data_storage.data_storage import DataStorage
from goit_i_pycore_i_personal_assistant.services.handlers_base.handler_output import HandlerOutput
from goit_i_pycore_i_personal_assistant.services.parse_input.parse_input import T_ARGS
from goit_i_pycore_i_personal_assistant.utils.format import format_error


class HandlerBase[ParsedArgs, OutputData](abc.ABC, BaseModel):
    """Base class for handlers.

    Used class, not function, because it must have the same signature for all handlers.

    Also, it is good to have some predefined structure.
    """

    args: T_ARGS

    data_storage: DataStorage

    console: rich.console.Console

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @abc.abstractmethod
    def _parse_args(self) -> ParsedArgs:
        """Parse command line arguments.

        Because it is better, at first, to validate input.
        """

    @abc.abstractmethod
    def _make_action(
        self,
        parsed_args: ParsedArgs,
    ) -> OutputData:
        """Make action based on parsed arguments."""

    @abc.abstractmethod
    def _get_or_render_output(
        self,
        output_data: OutputData,
    ) -> HandlerOutput:
        """Get or render output based on output data."""

    def run(self) -> HandlerOutput:
        try:
            parsed_args = self._parse_args()
            output_data = self._make_action(parsed_args)
            return self._get_or_render_output(output_data)
        except (InvalidCommandError, ValueError, KeyError) as exc:
            error_name = type(exc).__name__
            msg = str(exc)
            return HandlerOutput(
                message_rich=format_error(
                    error_name,
                    msg,
                ),
            )
