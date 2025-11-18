import datetime
import enum
from collections.abc import Callable
from typing import TYPE_CHECKING, Annotated, Any

from prompt_toolkit import HTML, prompt
from prompt_toolkit.shortcuts import choice
from pydantic import AfterValidator, BaseModel, ConfigDict, Field

from persyval.exceptions.main import InvalidCommandError
from persyval.services.console.types import PromptToolkitFormattedText
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
    DICT_BY_COMMA_AND_EQUAL = "dict_by_comma_and_equal"


type SELECT_OPTION[T] = tuple[T, PromptToolkitFormattedText]
type SELECT_OPTIONS[T] = list[SELECT_OPTION[T]]


@enum.unique
class ValueInteractiveMode(enum.StrEnum):
    TEXT_INPUT = "text_input"
    BOOL_INPUT = "bool_input"
    SELECT_FROM_OPTIONS = "select_from_options"
    CUSTOM = "custom"


type T_FIELD_NAME = str
type T_PARSE_RESULT_DICT = dict[T_FIELD_NAME, Any]


class ArgMetaConfig(BaseModel):
    name: str
    description: str | None = None

    alternative_text: str | None = None

    boolean_text: str | None = None

    type_: ArgType = ArgType.TEXT
    required: bool = False

    default: Any | None = None
    default_factory: Callable[[], Any] | None = None

    value_interactive_mode: ValueInteractiveMode | None = None
    value_interactive_options: SELECT_OPTIONS | None = None  # type: ignore[type-arg]  # pyright: ignore[reportMissingTypeArgument]
    value_interactive_custom_handler: Callable[[T_PARSE_RESULT_DICT], Any] | None = None

    format: str | None = None
    parser_func: Callable[[str], Any] | None = None
    validator_func: Callable[[Any], Any] | None = None

    allow_input_on_empty: bool = False

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


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

    def _parse_i_args_pre_validation(
        self,
        *,
        args: T_ARGS,
        non_interactive: bool,
    ) -> None:
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

    def parse(
        self,
        *,
        args: T_ARGS,
        non_interactive: bool = False,
    ) -> ParseResult:
        self._parse_i_args_pre_validation(
            args=args,
            non_interactive=non_interactive,
        )

        result_dict: T_PARSE_RESULT_DICT = {}
        for index, arg_meta_config in enumerate(self.args):
            try:
                arg = args[index]
            except IndexError:
                arg = None

            arg = handle_default_for_arg(
                arg_meta_config=arg_meta_config,
                arg=arg,
                non_interactive_guard=non_interactive,
            )

            # ---------

            if arg is None and non_interactive:
                continue

            # -----------

            prompt_text = create_prompt_text_for_arg(
                arg_meta_config=arg_meta_config,
                arg=arg,
            )

            # ----------

            arg = handle_input_on_empty_arg(
                arg_meta_config=arg_meta_config,
                arg=arg,
                prompt_text=prompt_text,
                result_dict=result_dict,
            )

            # ---------

            arg = handle_default_for_arg(
                arg_meta_config=arg_meta_config,
                arg=arg,
                # Note: Because we already not in interactive mode here, no need to guard again.
                non_interactive_guard=False,
            )

            # ---------

            if not arg and arg_meta_config.required:
                msg = f"Required argument `{arg_meta_config.name}` is missing."
                raise InvalidCommandError(msg)

            try:
                arg_result = parse_arg_to_arg_result(
                    arg_meta_config=arg_meta_config,
                    arg=arg,
                )
            except Exception as exc:
                msg = f"Can't parse argument `{arg_meta_config.name}`: {arg}"
                raise type(exc)(msg) from exc

            if arg_meta_config.validator_func:
                # noinspection PyUnboundLocalVariable
                arg_result = arg_meta_config.validator_func(arg_result)

            # noinspection PyUnboundLocalVariable
            result_dict[arg_meta_config.name] = arg_result

        return self.result_cls(**result_dict)


def handle_default_for_arg(
    *,
    arg_meta_config: ArgMetaConfig,
    arg: Any,  # noqa: ANN401
    non_interactive_guard: bool = False,
) -> Any:  # noqa: ANN401
    # TODO: (?) Rework check for None vs falsy values.
    if not arg:
        if arg_meta_config.default is not None:
            arg = arg_meta_config.default
        elif arg_meta_config.default_factory is not None:
            arg = arg_meta_config.default_factory()
        elif arg_meta_config.required and non_interactive_guard:
            msg = f"Required argument `{arg_meta_config.name}` is missing."
            raise InvalidCommandError(msg)

    return arg


def create_prompt_text_for_arg(
    arg_meta_config: ArgMetaConfig,
    arg: Any,  # noqa: ANN401
) -> str:
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

    return prompt_text


def handle_input_on_empty_arg(  # noqa: C901, PLR0912
    arg_meta_config: ArgMetaConfig,
    arg: Any,  # noqa: ANN401
    prompt_text: str,
    result_dict: T_PARSE_RESULT_DICT,
) -> Any:  # noqa: ANN401
    if not arg and arg_meta_config.allow_input_on_empty:
        value_interactive_mode = arg_meta_config.value_interactive_mode
        if not value_interactive_mode:
            if arg_meta_config.type_ == ArgType.BOOL:
                value_interactive_mode = ValueInteractiveMode.BOOL_INPUT
            elif arg_meta_config.type_ == ArgType.TEXT:
                value_interactive_mode = ValueInteractiveMode.TEXT_INPUT

        # ---------

        match value_interactive_mode:
            case ValueInteractiveMode.BOOL_INPUT:
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
            case ValueInteractiveMode.TEXT_INPUT:
                arg = prompt(HTML(prompt_text))
            case ValueInteractiveMode.SELECT_FROM_OPTIONS:
                if not arg_meta_config.value_interactive_options:  # pyright: ignore[reportUnknownMemberType]
                    msg = f"Argument `{arg_meta_config.name}` "
                    "is configured to select from options, but no options are provided."
                    raise InvalidCommandError(msg)

                selected = choice(  # pyright: ignore[reportUnknownVariableType]
                    message=f"Choose {arg_meta_config.name}: ",
                    options=arg_meta_config.value_interactive_options,  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
                )
                arg = selected  # pyright: ignore[reportUnknownVariableType]

            case ValueInteractiveMode.CUSTOM:
                if not arg_meta_config.value_interactive_custom_handler:
                    msg = f"Argument `{arg_meta_config.name}` "
                    "is configured to use a custom handler, but no handler is provided."
                    raise InvalidCommandError(msg)

                arg = arg_meta_config.value_interactive_custom_handler(result_dict)
            case None:
                pass

    return arg  # pyright: ignore[reportUnknownVariableType]


def parse_arg_to_arg_result(
    arg_meta_config: ArgMetaConfig,
    arg: Any,  # noqa: ANN401
) -> Any:  # noqa: ANN401
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
                arg_result = str(arg)
            case ArgType.INT:
                try:
                    arg_result = int(arg)
                except ValueError as exc:
                    msg = f"Invalid integer value: '{arg}'"
                    raise InvalidCommandError(msg) from exc
            case ArgType.BOOL:
                arg_result = convert_command_part_to_bool(arg)
            case ArgType.LIST_BY_COMMA:
                arg_result = parse_list(arg)  # pyright: ignore[reportUnknownArgumentType, reportUnknownVariableType]
            case ArgType.DICT_BY_COMMA_AND_EQUAL:
                arg_result = parse_dict(arg)
            case ArgType.DATE:
                arg_result = datetime.date.fromisoformat(arg)

    return arg_result


def parse_list(value: str | list[str]) -> list[str]:
    if isinstance(value, list):
        return value

    return list(filter(None, value.split(",")))


def parse_dict(value: str | dict[str, Any]) -> dict[str, str]:
    if isinstance(value, dict):
        return value

    result: dict[str, str] = {}

    for part in value.split(","):
        split = part.split("=")
        if len(split) != 2:  # noqa: PLR2004
            continue

        key, value = split
        result[key] = value

    return result
