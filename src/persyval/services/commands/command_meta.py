import enum
from typing import TYPE_CHECKING, Annotated, Any

from pydantic import AfterValidator, BaseModel, ConfigDict, Field

from persyval.exceptions.main import InvalidCommandError
from persyval.services.commands.commands_enum import Command
from persyval.services.handlers_base.handler_base import HandlerBase
from persyval.utils.convert_command_part_to_bool import convert_command_part_to_bool

if TYPE_CHECKING:
    from persyval.services.parse_input.parse_input import T_ARGS


class ArgType(enum.StrEnum):
    TEXT = "text"
    INT = "int"
    BOOL = "bool"


class ArgMetaConfig(BaseModel):
    name: str
    type_: ArgType = ArgType.TEXT
    required: bool = False


type T_ARGS_CONFIG = list[ArgMetaConfig]


def validate_order_of_args(args: T_ARGS_CONFIG) -> T_ARGS_CONFIG:
    saw_optional = False

    for arg_meta in args:
        if arg_meta.required:
            if saw_optional:
                msg = (
                    f"Required argument `{arg_meta.name}` appears after optional arguments. "
                    "All required arguments must come before optional ones."
                )
                raise ValueError(msg)
        else:
            saw_optional = True

    return args


class ArgsConfig[ParseResult](BaseModel):
    result_cls: type[ParseResult]
    args: Annotated[T_ARGS_CONFIG, AfterValidator(validate_order_of_args), Field(default_factory=list)]

    def parse(self, args: T_ARGS) -> ParseResult:
        if len(args) > len(self.args):
            msg = "Too many arguments provided."
            raise InvalidCommandError(msg)

        required_args_amount = len(
            list(filter(lambda arg_meta_config_local: arg_meta_config_local.required, self.args)),
        )
        if len(args) < required_args_amount:
            msg = "Not enough arguments provided."
            raise InvalidCommandError(msg)

        result_dict: dict[str, str | int | bool] = {}
        for arg_meta_config, arg in zip(self.args, args, strict=False):
            arg_type = arg_meta_config.type_

            arg_result: str | int | bool

            # noinspection PyUnreachableCode
            match arg_type:
                case ArgType.TEXT:
                    arg_result = arg
                case ArgType.INT:
                    arg_result = int(arg)
                case ArgType.BOOL:
                    arg_result = convert_command_part_to_bool(arg)
                case _:
                    msg = f"Unknown arg type: {arg_type}"
                    raise ValueError(msg)

            # noinspection PyUnboundLocalVariable
            result_dict[arg_meta_config.name] = arg_result

        return self.result_cls(**result_dict)


class CommandMeta(BaseModel):
    command: Command
    args_config: ArgsConfig[Any] | None = None
    description: str = Field(default="")
    handler: type[HandlerBase]

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
