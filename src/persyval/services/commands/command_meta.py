import enum

from pydantic import BaseModel, ConfigDict, Field

from persyval.services.commands.commands_enum import Command
from persyval.services.handlers_base.handler_base import HandlerBase


class ArgType(enum.StrEnum):
    TEXT = "text"
    INT = "int"
    BOOL = "bool"


class ArgMetaConfig(BaseModel):
    name: str
    type_: ArgType = ArgType.TEXT
    required: bool = False


class CommandMeta(BaseModel):
    command: Command
    args: list[ArgMetaConfig | str] = Field(default_factory=list)
    description: str = Field(default="")
    handler: type[HandlerBase]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
