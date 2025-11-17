import enum
from collections.abc import Callable
from typing import TYPE_CHECKING, Annotated, Any

from prompt_toolkit import HTML, prompt
from pydantic import AfterValidator, BaseModel, Field

from persyval.exceptions.main import InvalidCommandError
from persyval.services.console.yes_no_dialog import yes_no_skip_dialog
from persyval.utils.convert_command_part_to_bool import convert_command_part_to_bool

if TYPE_CHECKING:
    from persyval.services.parse_input.parse_input import T_ARGS


class ArgType(enum.StrEnum):
    TEXT = "text"
    INT = "int"
    BOOL = "bool"

    DATE = "date"

    LIST_BY_COMMA = "list_by_comma"


class ArgMetaConfig(BaseModel):
    name: str
    description: str | None = None

    alternative_text: str | None = None

    boolean_text: str | None = None

    type_: ArgType = ArgType.TEXT
    required: bool = False

    default: Any | None = None
    default_factory: Callable[[], Any] | None = None

    format: str | None = None
    parser_func: Callable[[str], Any] | None = None
    validator_func: Callable[[Any], Any] | None = None

    allow_input_on_empty: bool = False


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

    def reparse(
        self,
        *,
        parsed_args: ParseResult,
        non_interactive: bool = False,
    ) -> ParseResult:
        args: list[str | None] = []
        for arg_meta_config in self.args:
            arg = getattr(parsed_args, arg_meta_config.name)
            arg = str(arg) if arg else None
            args.append(arg)

        return self.parse(
            args=args,
            non_interactive=non_interactive,
        )

    def parse(  # noqa: C901, PLR0912, PLR0915
        self,
        *,
        args: T_ARGS,
        non_interactive: bool = False,
    ) -> ParseResult:
        # sourcery skip: low-code-quality
        if len(args) > len(self.args):
            msg = "Too many arguments provided."
            raise InvalidCommandError(msg)

        required_args_amount = len(
            list(filter(lambda arg_meta_config_local: arg_meta_config_local.required, self.args)),
        )
        if non_interactive and len(args) < required_args_amount:
            msg = "Not enough arguments provided."
            raise InvalidCommandError(msg)

        result_dict: dict[str, Any] = {}
        for index, arg_meta_config in enumerate(self.args):
            try:
                arg = args[index]
            except IndexError:
                arg = None

            if arg_meta_config.required and arg is None and non_interactive:
                if arg_meta_config.default is not None:
                    arg = arg_meta_config.default
                elif arg_meta_config.default_factory is not None:
                    arg = arg_meta_config.default_factory()
                else:
                    msg = f"Required argument `{arg_meta_config.name}` is missing."
                    raise InvalidCommandError(msg)

            if arg is None and non_interactive:
                continue

            # ---

            if arg_meta_config.alternative_text:
                prompt_text = arg_meta_config.alternative_text
            else:
                prompt_text = f"Enter <b>{arg_meta_config.name}</b>"
                if arg_meta_config.description:
                    prompt_text = f"{prompt_text} - {arg_meta_config.description}"
                if not arg_meta_config.required:
                    prompt_text = f"{prompt_text} <i>(optional)</i>"
                if arg_meta_config.format:
                    prompt_text = f"{prompt_text} <i>({arg_meta_config.format})</i>"
                if not arg and arg_meta_config.default:
                    prompt_text = f"{prompt_text} <i>(or skip for default: '{arg_meta_config.default}')</i>"
                if not arg and arg_meta_config.default_factory:
                    prompt_text = f"{prompt_text} <i>(or skip for default)</i>"
                prompt_text = f"{prompt_text}: "

            # ---

            if not arg and arg_meta_config.allow_input_on_empty:
                if arg_meta_config.type_ == ArgType.BOOL:
                    if arg_meta_config.alternative_text:
                        text = arg_meta_config.alternative_text
                    else:
                        text = f"Select '{arg_meta_config.name}'"
                        if arg_meta_config.description:
                            text = f"{text} - {arg_meta_config.description}"

                    value = yes_no_skip_dialog(
                        title=None if arg_meta_config.alternative_text else "Select value",
                        text=text,
                        boolean_text=arg_meta_config.boolean_text or "True/False",
                        optional=not arg_meta_config.required,
                    )
                    arg = str(value) if value is not None else None
                else:
                    arg = prompt(HTML(prompt_text))
                if not arg and arg_meta_config.default is not None:
                    arg = arg_meta_config.default
                if not arg and arg_meta_config.default_factory is not None:
                    arg = arg_meta_config.default_factory()

            if not arg and arg_meta_config.required:
                msg = f"Required argument `{arg_meta_config.name}` is missing."
                raise InvalidCommandError(msg)

            arg_result: Any

            if arg is None:
                arg_result = None
            elif arg_meta_config.parser_func:
                arg_result = arg_meta_config.parser_func(arg)
            else:
                arg_type = arg_meta_config.type_

                # noinspection PyUnreachableCode
                match arg_type:
                    case ArgType.TEXT:
                        arg_result = arg
                    case ArgType.INT:
                        try:
                            arg_result = int(arg)
                        except ValueError as exc:
                            msg = f"Invalid integer value: '{arg}'"
                            raise InvalidCommandError(msg) from exc
                    case ArgType.BOOL:
                        arg_result = convert_command_part_to_bool(arg)
                    case ArgType.LIST_BY_COMMA:
                        arg_result = list(filter(None, arg.split(",")))
                    case _:
                        msg = f"Unknown arg type: {arg_type}"
                        raise ValueError(msg)

            if arg_meta_config.validator_func:
                # noinspection PyUnboundLocalVariable
                arg_result = arg_meta_config.validator_func(arg_result)

            # noinspection PyUnboundLocalVariable
            result_dict[arg_meta_config.name] = arg_result

        return self.result_cls(**result_dict)
