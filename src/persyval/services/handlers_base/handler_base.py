import abc
from typing import Annotated

import rich
from pydantic import BaseModel, ConfigDict, Field

from persyval.exceptions.main import InvalidCommandError
from persyval.services.data_storage.data_storage import DataStorage
from persyval.services.handlers_base.handler_output import HandlerOutput
from persyval.services.parse_input.parse_input import T_ARGS
from persyval.utils.format import render_error


class HandlerBase(abc.ABC, BaseModel):
    """Base class for handlers.

    Used class, not function, because it must have the same signature for all handlers.

    Also, it is good to have some predefined structure.
    """

    args: T_ARGS

    data_storage: DataStorage

    console: rich.console.Console

    non_interactive: Annotated[bool, Field(description="For explicit non-interactive mode, if needed.")] = False
    plain_render: Annotated[
        bool,
        Field(description="For plain rendering, without extra-formatting. For non-interactive CLI."),
    ] = False

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @abc.abstractmethod
    def _handler(self) -> HandlerOutput | None:
        """Handler function.

        Parse command line arguments.

        Because it is better, at first, to validate input.

        ---

        Then interactively parse arguments if needed.

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
        try:
            return self._handler()
        except (InvalidCommandError, ValueError, KeyError, Exception) as exc:  # noqa: BLE001
            error_name = type(exc).__name__
            msg = str(exc)
            render_error(
                console=self.console,
                title=error_name,
                message=msg,
            )

            return HandlerOutput()
