from pydantic import BaseModel, ConfigDict, Field

from goit_i_pycore_i_personal_assistant.services.commands.commands_enum import Command
from goit_i_pycore_i_personal_assistant.services.handlers_base.handler_base import HandlerBase


class CommandMeta(BaseModel):
    command: Command
    args: list[str] = Field(default_factory=list)
    description: str = Field(default="")
    handler: type[HandlerBase]  # type: ignore[type-arg]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
