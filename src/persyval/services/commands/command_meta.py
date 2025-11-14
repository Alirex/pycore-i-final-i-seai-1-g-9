from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field

from persyval.services.commands.args_config import ArgsConfig
from persyval.services.commands.commands_enum import Command
from persyval.services.handlers_base.handler_base import HandlerBase


class CommandMeta(BaseModel):
    command: Command
    args_config: ArgsConfig[Any] | None = None
    description: str = Field(default="")
    handler: type[HandlerBase]  # type: ignore[type-arg]
    hidden: Annotated[bool, Field(description="Hidden from hints and basic help.")] = False

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
