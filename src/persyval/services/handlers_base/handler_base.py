import abc
import sys
from typing import TYPE_CHECKING, Annotated, Any

import rich
from pydantic import BaseModel, ConfigDict, Field

from persyval.exceptions.main import AlreadyExistsError, InvalidCommandError, InvalidDataError, NotFoundError
from persyval.services.data_storage.data_storage import DataStorage
from persyval.services.execution_queue.execution_queue import ExecutionQueue
from persyval.services.handlers_base.handler_output import HandlerOutput
from persyval.services.parse_input.parse_input import T_ARGS
from persyval.utils.format import render_error

if TYPE_CHECKING:
    from persyval.services.commands.command_meta import ArgsConfig


class HandlerBase[HandlerArgs](abc.ABC, BaseModel):
    """Base class for handlers.

    Used class, not function, because it must have the same signature for all handlers.

    Also, it is good to have some predefined structure.
    """

    args: T_ARGS

    execution_queue: ExecutionQueue

    data_storage: DataStorage

    console: rich.console.Console

    non_interactive: Annotated[bool, Field(description="For explicit non-interactive mode, if needed.")] = False
    plain_render: Annotated[
        bool,
        Field(description="For plain rendering, without extra-formatting. For non-interactive CLI."),
    ] = False
    terminal_simplified: Annotated[
        bool,
        Field(
            description="For simplified terminal input. For non-interactive CLI or when used not good enough terminal.",
        ),
    ] = False
    raise_sys_exit_on_error: bool = False
    throw_full_error: bool = False

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @abc.abstractmethod
    def _get_args_config(self) -> ArgsConfig[Any]:
        """Get arguments configuration."""

    def _handler(self) -> HandlerOutput | None:
        """Handler function.

        Parse command line arguments.

        Because it is better, at first, to validate input.


        """
        args_config = self._get_args_config()
        parsed_args = args_config.parse(self.args)
        return self._make_action(parsed_args)

    def parsed_call(self, parsed_args: HandlerArgs) -> HandlerOutput | None:
        return self._make_action(parsed_args)

    @abc.abstractmethod
    def _make_action(self, parsed_args: HandlerArgs) -> HandlerOutput | None:
        """Make action with parsed arguments.

        Interactively parse arguments if needed.

        Use `prompt-toolkit` or `rich` for interactive input.

        For example:
        - formatting (https://python-prompt-toolkit.readthedocs.io/en/latest/pages/printing_text.html)
        - choice (https://python-prompt-toolkit.readthedocs.io/en/latest/pages/asking_for_a_choice.html)
        - yes_no_dialog (https://python-prompt-toolkit.readthedocs.io/en/latest/pages/dialogs.html#yes-no-confirmation-dialog)
        - multiline input (https://python-prompt-toolkit.readthedocs.io/en/latest/pages/asking_for_input.html#multiline-input)

        ---

        Perfect if non-interactive logic is just a call to a function.

        ---

        Then get or render output based on output data.
        """

    def run(self) -> HandlerOutput | None:
        # sourcery skip: remove-redundant-exception
        try:
            return self._handler()
        except (
            InvalidCommandError,
            NotFoundError,
            AlreadyExistsError,
            InvalidDataError,
            ValueError,
            KeyError,
            Exception,
        ) as exc:
            error_name = type(exc).__name__
            msg = str(exc)
            render_error(
                console=self.console,
                title=error_name,
                message=msg,
            )

            if self.throw_full_error:
                raise

            if self.raise_sys_exit_on_error:
                sys.exit(1)

            return HandlerOutput()
