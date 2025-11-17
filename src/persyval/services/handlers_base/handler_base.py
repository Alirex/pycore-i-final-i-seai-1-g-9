import abc
import sys
from typing import TYPE_CHECKING, Annotated

import rich
from pydantic import BaseModel, ConfigDict, Field

from persyval.exceptions.main import AlreadyExistsError, InvalidCommandError, InvalidDataError, NotFoundError
from persyval.services.data_storage.data_storage import DataStorage
from persyval.services.execution_queue.execution_queue import ExecutionQueue
from persyval.services.handlers_base.handler_output import HandlerOutput
from persyval.utils.format import render_error

if TYPE_CHECKING:
    from persyval.services.commands.args_config import ArgsConfig
    from persyval.services.parse_input.parse_input import T_ARGS


class HandlerBase[HandlerArgs](abc.ABC, BaseModel):
    """Base class for handlers.

    Used class, not function, because it must have the same signature for all handlers.

    Also, it is good to have some predefined structure.
    """

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
    def _get_args_config(self) -> ArgsConfig[HandlerArgs]:
        """Get arguments configuration."""

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

    def _handle_parsed_args(
        self,
        args: T_ARGS | None,
        parsed_args: HandlerArgs | None,
    ) -> HandlerArgs:
        if (args is None and parsed_args is None) or (args is not None and parsed_args is not None):
            msg = "Either args or parsed_args must be provided."
            raise ValueError(msg)

        args_config = self._get_args_config()
        # Parse command line arguments.
        #   Because it is better, at first, to validate input.

        if parsed_args is None and args is not None:
            reparsed_args = args_config.parse(args=args, non_interactive=self.non_interactive)
        elif args is None and parsed_args is not None:
            reparsed_args = args_config.reparse(parsed_args=parsed_args, non_interactive=self.non_interactive)
        else:
            msg = "Either args or parsed_args must be provided."
            raise ValueError(msg)

        return reparsed_args

    def run(
        self,
        args: T_ARGS | None,
        parsed_args: HandlerArgs | None = None,
    ) -> HandlerOutput | None:
        # sourcery skip: assign-if-exp, remove-redundant-exception

        try:
            result = self._make_action(
                parsed_args=self._handle_parsed_args(args, parsed_args),
            )

        except (
            InvalidCommandError,
            NotFoundError,
            AlreadyExistsError,
            InvalidDataError,
            ValueError,
            KeyError,
            Exception,  # noqa: BLE001
        ) as exc:
            return self._handle_exception(exc)

        return result

    def _handle_exception(self, exc: Exception) -> HandlerOutput | None:
        error_name = type(exc).__name__
        msg = str(exc)
        render_error(
            console=self.console,
            title=error_name,
            message=msg,
        )

        if self.throw_full_error:
            raise exc

        if self.raise_sys_exit_on_error:
            sys.exit(1)

        return HandlerOutput()
