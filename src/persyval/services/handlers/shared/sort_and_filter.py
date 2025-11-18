import datetime
import enum
from typing import TYPE_CHECKING, Any

from prompt_toolkit import prompt
from pydantic import BaseModel, Field

from persyval.models.contact import Contact
from persyval.models.note import Note
from persyval.services.birthday.parse_and_format import format_birthday_for_edit_and_export
from persyval.services.commands.args_config import (
    T_PARSE_RESULT_DICT,
    ArgMetaConfig,
    ArgsConfig,
    ArgType,
    ValueInteractiveMode,
)
from persyval.services.execution_queue.execution_queue import HandlerArgsBase
from persyval.services.model_meta.field_meta import FilterMode
from persyval.services.model_meta.model_meta_info import HaveMetaInfoProtocol

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable


@enum.unique
class ListOrderModeEnum(enum.StrEnum):
    DEFAULT = enum.auto()
    CUSTOM = enum.auto()


@enum.unique
class ListFilterModeEnum(enum.StrEnum):
    ALL = enum.auto()
    FILTER = enum.auto()


class ListModeMeta[T](BaseModel):
    mode: T
    title: str


ListFilterModeMeta = ListModeMeta[ListFilterModeEnum]
ListOrderModeMeta = ListModeMeta[ListOrderModeEnum]


class ListIArgs(HandlerArgsBase):
    order_mode: ListOrderModeEnum | None = None
    order_query: list[str] | None = None

    filter_mode: ListFilterModeEnum | None = None
    filter_query: dict[str, Any] | None = None


LIST_FILTER_MODE_REGISTRY: dict[ListFilterModeEnum, ListFilterModeMeta] = {
    item.mode: item
    for item in [
        ListFilterModeMeta(
            mode=ListFilterModeEnum.ALL,
            title="Show all",
        ),
        ListFilterModeMeta(
            mode=ListFilterModeEnum.FILTER,
            title="Filter",
        ),
    ]
}


LIST_ORDER_MODE_REGISTRY: dict[ListOrderModeEnum, ListOrderModeMeta] = {
    item.mode: item
    for item in [
        ListOrderModeMeta(
            mode=ListOrderModeEnum.DEFAULT,
            title="Use default",
        ),
        ListOrderModeMeta(
            mode=ListOrderModeEnum.CUSTOM,
            title="Customize",
        ),
    ]
}


def value_interactive_custom_i_filter_query_i_wrapper(
    model: type[HaveMetaInfoProtocol],
) -> Callable[[T_PARSE_RESULT_DICT], str]:
    def handler(parsed: T_PARSE_RESULT_DICT) -> str:
        if parsed.get("filter_mode") != ListFilterModeEnum.FILTER:
            return ""

        field_names = model.get_meta_info().fields_meta_config.get_field_names_for_filtering()

        message = f"Enter queries to filter by. \nFormat: key=value,key2=value2 \nAllowed keys: {', '.join(sorted(field_names))}\n"  # noqa: E501
        return prompt(
            message=message,
        )

    return handler


def validate_filter_query_i_wrapper(model: type[HaveMetaInfoProtocol]) -> Callable[[dict[str, str]], dict[str, Any]]:
    def validator(value: dict[str, str]) -> dict[str, Any]:
        meta_config = model.get_meta_info().fields_meta_config

        new_dict: dict[str, Any] = {}
        for key, val in value.items():
            try:
                fact_name = meta_config.get_field_name_fact(key)
            except KeyError:
                msg = f"Filtering by '{key}' is not allowed."
                raise KeyError(msg) from None

            new_dict[fact_name] = val

        return new_dict

    return validator


def value_interactive_custom_i_order_query_i_wrapper(
    model: type[HaveMetaInfoProtocol],
) -> Callable[[T_PARSE_RESULT_DICT], str]:
    def handler(parsed: T_PARSE_RESULT_DICT) -> str:
        if parsed.get("order_mode") != ListOrderModeEnum.CUSTOM:
            return ""

        field_names = model.get_meta_info().fields_meta_config.get_field_names_for_filtering()

        message = (
            "Enter queries to order by. \n"
            "Format: key,-key2 \n"
            "Add '-' before key to sort in descending order. \n"
            "If field has multiple values, sorting will be done by the order of values. \n"
            f"Allowed keys: {', '.join(sorted(field_names))}\n"
        )

        return prompt(
            message=message,
        )

    return handler


def validate_order_query_i_wrapper(model: type[HaveMetaInfoProtocol]) -> Callable[[list[str]], list[str]]:
    def validator(value: list[str]) -> list[str]:
        meta_config = model.get_meta_info().fields_meta_config

        new_list: list[str] = []
        for item in value:
            key = item.lstrip("-")

            try:
                fact_name = meta_config.get_field_name_fact(key)
            except KeyError:
                msg = f"Ordering by '{key}' is not allowed."
                raise KeyError(msg) from None

            item_local = f"-{fact_name}" if item.startswith("-") else fact_name

            new_list.append(item_local)

        return new_list

    return validator


def collect_args_config_i_for_model(
    model: type[HaveMetaInfoProtocol],
) -> ArgsConfig[ListIArgs]:
    return ArgsConfig[ListIArgs](
        result_cls=ListIArgs,
        args=[
            ArgMetaConfig(
                name="order_mode",
                parser_func=lambda x: ListOrderModeEnum(x) if x else None,
                allow_input_on_empty=True,
                value_interactive_mode=ValueInteractiveMode.SELECT_FROM_OPTIONS,
                value_interactive_options=[(item.mode, item.title) for item in LIST_ORDER_MODE_REGISTRY.values()],
            ),
            ArgMetaConfig(
                name="order_query",
                type_=ArgType.LIST_BY_COMMA,
                default_factory=list,
                allow_input_on_empty=True,
                value_interactive_mode=ValueInteractiveMode.CUSTOM,
                #
                value_interactive_custom_handler=value_interactive_custom_i_order_query_i_wrapper(model),
                validator_func=validate_order_query_i_wrapper(model),
            ),
            ArgMetaConfig(
                name="filter_mode",
                parser_func=lambda x: ListFilterModeEnum(x) if x else None,
                allow_input_on_empty=True,
                value_interactive_mode=ValueInteractiveMode.SELECT_FROM_OPTIONS,
                value_interactive_options=[(item.mode, item.title) for item in LIST_FILTER_MODE_REGISTRY.values()],
            ),
            ArgMetaConfig(
                name="filter_query",
                type_=ArgType.DICT_BY_COMMA_AND_EQUAL,
                default_factory=dict,
                allow_input_on_empty=True,
                value_interactive_mode=ValueInteractiveMode.CUSTOM,
                #
                value_interactive_custom_handler=value_interactive_custom_i_filter_query_i_wrapper(model),
                validator_func=validate_filter_query_i_wrapper(model),
            ),
        ],
    )


LIST_I_ARGS_CONFIG_CONTACTS = collect_args_config_i_for_model(model=Contact)

LIST_I_ARGS_CONFIG_NOTES = collect_args_config_i_for_model(model=Note)


class ListConfig(BaseModel):
    order_mode: ListOrderModeEnum | None = None
    order_query: list[str] = Field(default_factory=list)

    filter_mode: ListFilterModeEnum | None = None
    filter_query: dict[str, str] = Field(default_factory=dict)


def validate_filter_query_in_data_action(
    model: HaveMetaInfoProtocol,
    filter_query: dict[str, Any],
) -> dict[str, Any]:
    meta_config = model.get_meta_info().fields_meta_config

    new_dict: dict[str, Any] = {}
    for key, val in filter_query.items():
        try:
            fact_name = meta_config.get_field_name_fact(key)
        except KeyError:
            msg = f"Filtering by '{key}' is not allowed."
            raise KeyError(msg) from None

        parse_func = None
        for field in meta_config.fields:
            if field.name == fact_name:
                parse_func = field.parse_func
                break

        val_fact = parse_func(val) if parse_func is not None else val.lower()

        new_dict[fact_name] = val_fact

    return new_dict


def filter_iterable[T: HaveMetaInfoProtocol](  # noqa: C901, PLR0912
    iterable: Iterable[T],
    model: type[T],
    list_config: ListConfig,
) -> list[Any]:
    filter_mode = list_config.filter_mode

    result: list[T]
    match filter_mode:
        case ListFilterModeEnum.ALL:
            result = list(iterable)
        case ListFilterModeEnum.FILTER:
            filter_query = validate_filter_query_in_data_action(
                model=model,
                filter_query=list_config.filter_query,
            )

            fields_meta_registry = model.get_meta_info().fields_meta_config.get_fields_meta_registry()

            result = []
            for item in iterable:
                is_good = True
                for field_name, filter_value in filter_query.items():
                    field_meta = fields_meta_registry[field_name]

                    field_value = getattr(item, field_meta.name)

                    if field_value is None:
                        is_good = False
                        break

                    match field_meta.filter_mode:
                        case FilterMode.EXACT:
                            if field_meta.is_list_based:
                                if not any(filter_value == str(item).lower() for item in field_value):
                                    is_good = False
                                    break

                            elif filter_value != str(field_value).lower():
                                is_good = False
                                break
                            continue

                        case FilterMode.PARTIAL:
                            if field_meta.is_list_based:
                                if not any(filter_value in str(item).lower() for item in field_value):
                                    is_good = False
                                    break

                            elif filter_value not in str(field_value).lower():
                                is_good = False
                                break

                    continue

                if is_good:
                    result.append(item)

        case None:
            msg = "Filter mode is not specified."
            raise ValueError(msg)

    order_mode = list_config.order_mode
    match order_mode:
        case ListOrderModeEnum.DEFAULT:
            return result
        case ListOrderModeEnum.CUSTOM:
            order_query = list_config.order_query

            # Sort by lower() if the field is str

            for order_field in reversed(order_query):
                is_descending = order_field.startswith("-")
                field_name = order_field.lstrip("-")

                result.sort(
                    key=lambda item: normalize_sort_value(getattr(item, field_name)),
                    reverse=is_descending,
                )

        case None:
            msg = "Order mode is not specified."
            raise ValueError(msg)

    return result


def normalize_sort_value(
    value: Any,  # noqa: ANN401
) -> Any:  # noqa: ANN401
    if isinstance(value, str):
        return value.lower()

    if value is None:
        return ""

    if isinstance(value, datetime.date):
        return format_birthday_for_edit_and_export(value)

    return value
