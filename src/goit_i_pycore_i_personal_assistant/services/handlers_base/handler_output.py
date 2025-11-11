from pydantic import BaseModel, Field

from goit_i_pycore_i_personal_assistant.services.console.types import RichFormattedText

# TODO: (?) Add support for `prompt_toolkit`
#   https://python-prompt-toolkit.readthedocs.io/en/3.0.52/pages/printing_text.html


class HandlerOutput(BaseModel):
    message_rich: RichFormattedText | None = Field(
        default=None,
        description="Output message, that will be displayed to the user. Rich formatted.",
    )
    is_exit: bool = Field(default=False, description="Exit the program")
